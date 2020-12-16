from project.database.models import Qhawax, EcaNoise, QhawaxInstallationHistory, Company, Bitacora
import project.main.business.get_business_helper as get_business_helper
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db
import dateutil.parser
import datetime
import dateutil

session = db.session

def updateMainIncaQhawaxTable(new_main_inca, qhawax_name):
    """ Helper qHAWAX function to save main inca value in qHAWAX table """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'main_inca': new_main_inca})
        session.commit()

def updateMainIncaQhawaxInstallationTable(new_main_inca, qhawax_name):
    """ Helper qHAWAX function to save main inca value in qHAWAX Installation table """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                                 update(values={'main_inca': new_main_inca})
        session.commit()

def saveStatusOffQhawaxInstallationTable(qhawax_name,qhawax_lost_timestamp):
    """ Set qHAWAX OFF in qHAWAX Installation table """
    installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': -1,'last_registration_time_zone':qhawax_lost_timestamp})
        session.commit()

def saveStatusQhawaxTable(qhawax_name, qhawax_status,main_inca):
    """ Set qHAWAX ON or OFF in qHAWAX table """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).\
                              update(values={'state': qhawax_status,'main_inca':main_inca})
        session.commit()

def saveTurnOnLastTime(qhawax_name):
    """ Set qHAWAX ON in qHAWAX Installation table  """
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': 0, \
                               'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()

def turnOnAfterCalibration(qhawax_name):
    """ Set qHAWAX ON in qHAWAX Installation table"""
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()

def saveEndWorkFieldDate(qhawax_name,end_date):
    """ Save End Work in Field"""
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                                 update(values={'end_date_zone': end_date})
        session.commit()

def setAvailabilityQhawax(qhawax_name, availability):
    """ Update qHAWAX Availability to Occupied or Free """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'availability': availability})
        session.commit()

def changeMode(qhawax_name, mode):
    """Change To Other Mode"""
    if(isinstance(mode, str) is not True):
        raise TypeError("Mode value "+str(mode)+" should be string")

    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'mode': mode})
        session.commit()

def updateQhawaxInstallation(data):
    """ Update qHAWAX in Field """
    if(isinstance(data, dict) is not True):
        raise TypeError("qHAWAX Installation data "+str(data)+" should be in Json Format")
    if(util_helper.areFieldsValid(data)==False):
        raise Exception("qHAWAX Installation fields must have data")

    data['qhawax_id'] = same_helper.getQhawaxID(data['qhawax_name'])
    data.pop('qhawax_name', None)

    session.query(QhawaxInstallationHistory). \
            filter_by(qhawax_id=data['qhawax_id'], \
                      company_id=data['company_id'], \
                      end_date_zone=None).update(values=data)
    session.commit()

def createQhawax(qhawax_name,qhawax_type):
    """ Create a qHAWAX module """
    if(isinstance(qhawax_name, str) and isinstance(qhawax_type, str)):
        qhawax_data = {'name': qhawax_name, 'qhawax_type': qhawax_type,
                       'state': 'OFF', 'availability': "Available", 'main_inca':-1.0, 
                       'main_aqi':-1.0,'mode':"Stand By",'on_loop':0}
        qhawax_data_var = Qhawax(**qhawax_data)
        session.add(qhawax_data_var)
        session.commit()
    else:
        raise TypeError("qHAWAX name and type should be string")

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
        qhawax_installation = QhawaxInstallationHistory(**data)
        session.add(qhawax_installation)
        session.commit()

def writeBinnacle(qhawax_name,description,person_in_charge):
    """ Write observations in Binnacle"""

    if(isinstance(description, str) is not True):
        raise TypeError("Binnacle description should be string")

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        bitacora = {'timestamp_zone': datetime.datetime.now(dateutil.tz.tzutc()), \
                    'observation_type': 'Interna','description': description,  \
                    'qhawax_id':qhawax_id,'solution':None,'person_in_charge':person_in_charge, \
                    'end_date_zone':None,'start_date_zone':None}
        bitacora_update = Bitacora(**bitacora)
        session.add(bitacora_update)
        session.commit()

def util_qhawax_installation_set_up(qhawax_name,availability,mode,description,person_in_charge):
    setAvailabilityQhawax(qhawax_name,availability)
    changeMode(qhawax_name, mode)
    writeBinnacle(qhawax_name,description,person_in_charge)

def updateTimeOffWithLastTurnOff(last_time_of_turn_off_binnacle, qhawax_name):
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
            update(values={'last_registration_time_zone':last_time_of_turn_off_binnacle})
    session.commit()

def reset_on_loop(qhawax_name, loop):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    session.query(Qhawax). \
            filter_by(id=qhawax_id). \
            update(values={'on_loop':loop})
    session.commit()

def record_first_time_loop(qhawax_name, timestamp):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    session.query(Qhawax). \
            filter_by(id=qhawax_id). \
            update(values={'first_time_loop':timestamp})
    session.commit()