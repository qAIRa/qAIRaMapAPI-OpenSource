from project.database.models import Qhawax, EcaNoise, QhawaxInstallationHistory, Company, Bitacora
import project.main.business.get_business_helper as get_business_helper
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db
import dateutil.parser
import datetime
import dateutil

session = db.session
now = datetime.datetime.now(dateutil.tz.tzutc())

def updateMainIncaQhawaxTable(new_main_inca, qhawax_name):
    """ Helper qHAWAX function to save main inca value in qHAWAX table """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")
    qhawax_json_main_inca = {'main_inca': new_main_inca}
    same_helper.qhawaxQueryUpdate(qhawax_json_main_inca,qhawax_name)

def saveStatusQhawaxTable(qhawax_name, qhawax_status,main_inca):
    """ Set qHAWAX ON or OFF in qHAWAX table """
    if(type(main_inca) not in [int]):
        raise TypeError("Inca value "+str(main_inca)+" should be int")

    if(isinstance(qhawax_status, str) is not True):
        raise TypeError("Status value "+str(qhawax_status)+" should be string")

    qhawax_json_status = {'state': qhawax_status,'main_inca':main_inca}
    same_helper.qhawaxQueryUpdate(qhawax_json_status,qhawax_name)

def setAvailabilityQhawax(qhawax_name, availability):
    """ Update qHAWAX Availability to Occupied or Free """
    if(isinstance(availability, str) is not True):
        raise TypeError("Availability value "+str(availability)+" should be string")

    qhawax_json_availability = {'availability': availability}
    same_helper.qhawaxQueryUpdate(qhawax_json_availability,qhawax_name)

def changeMode(qhawax_name, mode):
    """Change To Other Mode"""
    if(isinstance(mode, str) is not True):
        raise TypeError("Mode value "+str(mode)+" should be string")

    qhawax_json_mode = {'mode': mode}
    same_helper.qhawaxQueryUpdate(qhawax_json_mode,qhawax_name)

def updateMainIncaQhawaxInstallationTable(new_main_inca, qhawax_name):
    """ Helper qHAWAX function to save main inca value in qHAWAX Installation table """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    qhawax_json_main_inca_installation = {'main_inca': new_main_inca}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_main_inca_installation,qhawax_name)

def saveStatusOffQhawaxInstallationTable(qhawax_name,qhawax_lost_timestamp):
    """ Set qHAWAX OFF in qHAWAX Installation table """
    qhawax_json_status_off = {'main_inca': -1,'last_registration_time_zone':qhawax_lost_timestamp}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_status_off,qhawax_name)

def saveTurnOnLastTime(qhawax_name):
    """ Set qHAWAX ON in qHAWAX Installation table  """
    qhawax_json_on = {'main_inca': 0, 'last_time_physically_turn_on_zone': now.replace(tzinfo=None)}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_on,qhawax_name)

def turnOnAfterCalibration(qhawax_name):
    """ Set qHAWAX ON in qHAWAX Installation table"""
    qhawax_json_on_after_calibration = {'last_time_physically_turn_on_zone': now.replace(tzinfo=None)}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_on_after_calibration,qhawax_name)

def saveEndWorkFieldDate(qhawax_name,end_date):
    """ Save End Work in Field"""
    qhawax_json_end_field = {'end_date_zone': end_date}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_end_field,qhawax_name)

def updateTimeOffWithLastTurnOff(time_turn_off_binnacle, qhawax_name):
    qhawax_json_last_turn_off = {'last_registration_time_zone':time_turn_off_binnacle}
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_last_turn_off,qhawax_name)

def updateQhawaxInstallation(data):
    """ Update qHAWAX in Field """
    if(isinstance(data, dict) is not True):
        raise TypeError("qHAWAX Installation data "+str(data)+" should be in Json Format")
    if(util_helper.areFieldsValid(data)==False):
        raise Exception("qHAWAX Installation fields must have data")

    data['qhawax_id'] = same_helper.getQhawaxID(data['qhawax_name'])
    data.pop('qhawax_name', None)

    session.query(QhawaxInstallationHistory). \
            filter_by(qhawax_id=data['qhawax_id'],company_id=data['company_id'],end_date_zone=None).update(values=data)
    session.commit()

def createQhawax(qhawax_name,qhawax_type):
    """ Create a qHAWAX module """
    if(isinstance(qhawax_name, str) is not True or isinstance(qhawax_type, str) is not True):
        raise TypeError("qHAWAX name and type should be string")

    qhawax_data = {'name': qhawax_name, 'qhawax_type': qhawax_type,'state': 'OFF', 'availability': "Available",
                   'main_aqi':-1.0,'mode':"Stand By",'on_loop':0,  'main_inca':-1.0}
    qhawax_data_var = Qhawax(**qhawax_data)
    session.add(qhawax_data_var)
    session.commit()

def createCompany(json_company):
    """ To insert new company"""
    if(isinstance(json_company, dict) is not True):
        raise TypeError("The Json company "+str(json_company)+" should be in Json Format")

    company_name = json_company.pop('company_name', None)
    json_company['name'] = company_name
    company_var = Company(**json_company)
    session.add(company_var)
    session.commit()

def storeNewQhawaxInstallation(data):
    """Insert new qHAWAX in Field  """
    if(isinstance(data, dict) is not True):
        raise TypeError("The Json company "+str(data)+" should be in Json Format")

    if(util_helper.areFieldsValid(data)==False):
        raise Exception("qHAWAX Installation fields have to have data")

    qhawax_id = same_helper.getQhawaxID(data['qhawax_name'])

    if(qhawax_id!=None):
        data['qhawax_id'] = int(qhawax_id)
        data['main_inca'] = same_helper.getMainIncaQhawaxTable(data['qhawax_id'])
        data['installation_date_zone'] = data['instalation_date']
        data['last_time_physically_turn_on_zone'] = data['instalation_date']
        data.pop('instalation_date', None)
        data.pop('qhawax_name', None)
        if('id' in data):
            data.pop('id', None)
        if('company_name' in data):
            data.pop('company_name', None)
        qhawax_installation = QhawaxInstallationHistory(**data)
        session.add(qhawax_installation)
        session.commit()

def writeBinnacle(qhawax_name,description,person_in_charge):
    """ Write observations in Binnacle"""
    if(isinstance(description, str) is not True):
        raise TypeError("Binnacle description should be string")

    if(isinstance(person_in_charge, str) is not True):
        raise TypeError("Binnacle person_in_charge should be string")

    qHAWAX_ID = same_helper.getQhawaxID(qhawax_name)
    if(qHAWAX_ID is not None):
        bitacora = {'timestamp_zone': now, 'observation_type': 'Interna','description': description, 'qhawax_id':qHAWAX_ID,\
                    'solution':None,'person_in_charge':person_in_charge, 'end_date_zone':None,'start_date_zone':None}
        bitacora_update = Bitacora(**bitacora)
        session.add(bitacora_update)
        session.commit()

def util_qhawax_installation_set_up(qhawax_name,availability,mode,description,person_in_charge):
    setAvailabilityQhawax(qhawax_name,availability)
    changeMode(qhawax_name, mode)
    writeBinnacle(qhawax_name,description,person_in_charge)

def reset_on_loop(qhawax_name, loop):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values={'on_loop':loop})
        session.commit()

def record_first_time_loop(qhawax_name, timestamp):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        session.query(Qhawax).filter_by(id=qhawax_id).update(values={'first_time_loop':timestamp})
        session.commit()