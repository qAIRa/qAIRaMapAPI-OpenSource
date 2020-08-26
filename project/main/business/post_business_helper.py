import datetime
import dateutil
import dateutil.parser
from project import app, db
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
import project.main.business.get_business_helper as get_business_helper

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, AirQualityMeasurement, Bitacora

var_gases=['CO','H2S','NO','NO2','O3','SO2']

session = db.session

def updateOffsetsFromProductID(qhawax_name, offsets):
    """
    Helper Gas Sensor function to save offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        if(isinstance(offsets, dict)):
            qhawax_id = same_helper.getQhawaxID(qhawax_name)
            for sensor_type in offsets:
                session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).\
                                         update(values=offsets[sensor_type])
            session.commit()
        else:
            raise TypeError("Offset "+str(offsets)+" should be in Json Format")
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def updateControlledOffsetsFromProductID(qhawax_name, controlled_offsets):
    """
    Helper Gas Sensor function to save controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        if(isinstance(controlled_offsets, dict)):
            qhawax_id = same_helper.getQhawaxID(qhawax_name)
            for sensor_type in controlled_offsets:
                session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).\
                                         update(values=controlled_offsets[sensor_type])
            session.commit()
        else:
            raise TypeError("Controlled Offset "+str(controlled_offsets)+" should be in Json Format")
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")


def updateNonControlledOffsetsFromProductID(qhawax_name, non_controlled_offsets):
    """
    Helper Gas Sensor function to save non controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        if(isinstance(non_controlled_offsets, dict)):
            qhawax_id = same_helper.getQhawaxID(qhawax_name)
            for sensor_type in non_controlled_offsets:
                session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).\
                                         update(values=non_controlled_offsets[sensor_type])
            session.commit()
        else:
            raise TypeError("Non Controlled Offset "+str(non_controlled_offsets)+" should be in Json Format")
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def updateMainIncaQhawaxTable(new_main_inca, qhawax_name):
    """
    Helper qHAWAX function to save main inca value in qHAWAX table

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type new_main_inca: integer
    :param new_main_inca: qHAWAX main inca

    """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(isinstance(qhawax_name, str)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'main_inca': new_main_inca})
        session.commit()
    else:
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

def updateMainIncaQhawaxInstallationTable(new_main_inca, qhawax_name):
    """
    Helper qHAWAX function to save main inca value in qHAWAX Installation table

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type new_main_inca: integer
    :param new_main_inca: qHAWAX main inca

    """
    if(type(new_main_inca) not in [int]):
        raise TypeError("Inca value "+str(new_main_inca)+" should be int")

    if(isinstance(qhawax_name, str)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                                 update(values={'main_inca': new_main_inca})
        session.commit()
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def saveStatusOffQhawaxTable(qhawax_name):
    """
    Set qHAWAX OFF in qHAWAX table
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'state': "OFF",'main_inca':-1})
        session.commit()
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def saveStatusOffQhawaxInstallationTable(qhawax_name,qhawax_lost_timestamp):
    """
    Set qHAWAX OFF in qHAWAX Installation table
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_lost_timestamp: timestamp
    :param qhawax_lost_timestamp: qHAWAX last time off

    """
    if(isinstance(qhawax_name, str)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': -1,'last_registration_time_zone':qhawax_lost_timestamp})
        session.commit()
    else:
        raise TypeError("The qHAWAX name "+str(qhawax_name)+" should be string")

def saveStatusOnTable(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX table
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'state': "ON",'main_inca':0})
        session.commit()
    else:
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

def saveTurnOnLastTime(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX Installation table
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'main_inca': 0,'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()
    else:
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

def turnOnAfterCalibration(qhawax_name):
    """
    Set qHAWAX ON in qHAWAX Installation table
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
        now = datetime.datetime.now(dateutil.tz.tzutc())
        session.query(QhawaxInstallationHistory).\
                filter_by(id=installation_id).\
                update(values={'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
        session.commit()
    else:
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

def setOccupiedQhawax(qhawax_id):
    """
    Update qHAWAX Availability to Occupied

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX ID "+str(qhawax_id)+" should be int")
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Occupied'})
    session.commit()

def setModeCustomer(qhawax_id):
    """
    Update qHAWAX mode to Customer

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX ID "+str(qhawax_id)+" should be int")
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'mode': "Cliente"})
    session.commit()

def saveEndWorkFieldDate(qhawax_id,end_date):
    """
    Save End Work in Field

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type end_date: timestamp
    :param end_date: qHAWAX installation end date

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX ID "+str(qhawax_id)+" should be int")
    installation_id = helper.getInstallationId(qhawax_id)
    session.query(QhawaxInstallationHistory).filter_by(id=installation_id).\
                                             update(values={'end_date_zone': end_date})
    session.commit()

def setAvailableQhawax(qhawax_id):
    """
    Update qhawax installation state in qHAWAX table

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX ID "+str(qhawax_id)+" should be int")
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Available'})
    session.commit()


def changeMode(qhawax_name, mode):
    """
    Change To Other Mode

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        if(isinstance(mode, str)):
            session.query(Qhawax).filter_by(name=qhawax_name).update(values={'mode': mode})
            session.commit()
        else:
            raise TypeError("Mode value "+str(qhawax_name)+" should be string")
    else:
        raise TypeError("qHAWAX name "+str(qhawax_name)+" should be string")

def updateQhawaxInstallation(data):
    """
    Update qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(util_helper.areFieldsValid(data)==True):
        session.query(QhawaxInstallationHistory). \
                filter_by(qhawax_id=data['qhawax_id'], \
                          company_id=data['company_id'], \
                          end_date=None).update(values=data)
        session.commit()
    else:
        raise Exception("qHAWAX Installation fields must have data")

def createQhawax(qhawax_id, qhawax_name,qhawax_type):
    """
    Create a qHAWAX module 
    
    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_type: string
    :param qhawax_type: qHAWAX type

    """
    if(type(qhawax_id) not in [int]):
        raise TypeError("qHAWAX id should be integer")
    
    if(isinstance(qhawax_name, str) and isinstance(qhawax_type, str)):
        qhawax_data = {'id':qhawax_id,'name': qhawax_name, 'qhawax_type': qhawax_type,
                       'state': 'OFF', 'availability': "Available", 'main_inca':-1.0, 
                       'main_aqi':-1.0,'mode':"Stand By"}
        qhawax_data_var = Qhawax(**qhawax_data)
        session.add(qhawax_data_var)
        session.commit()
    else:
        raise TypeError("qHAWAX name and type should be string")


def insertDefaultOffsets(last_gas_sensor_id, qhawax_name):
    """
    To insert a Default Offset 
    
    :type last_gas_sensor_id: integer
    :param last_gas_sensor_id: last gas sensor ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(verifyIfQhawaxExistBaseOnName(qhawax_name)):
        initial_serial_number = int(qhawax_id)*100
        start = 1
        for index in range(len(var_gases)):
            sensor_data = {'id':int(last_gas_sensor_id)+start, 'qhawax_id':qhawax_id, 
                           'serial_number': initial_serial_number + start, 'type': var_gases[index],
                           'WE': 0.0, 'AE': 0.0,'sensitivity': 0.0, 'sensitivity_2': 0.0,
                           'C0':0.0,'C1':0.0,'C2':0.0,'NC0':0.0,'NC1':0.0}
            sensor_data_var = GasSensor(**sensor_data)
            session.add(sensor_data_var)
            session.commit()
            start+=1

def createCompany(json_company):
    """
    To insert new company
    
    :type json_company: json
    :param json_company: json company

    """
    if(isinstance(json_company, dict)):
        company_name = json_company.pop('company_name', None)
        json_company['name'] = company_name
        company_var = Company(**json_company)
        session.add(company_var)
        session.commit()
    else:
        raise TypeError("The Json company "+str(json_company)+" should be in Json Format")

def storeNewQhawaxInstallation(data):
    """
    Insert new qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(isinstance(data, dict)):
        if(util_helper.areFieldsValid(data)==True):
            data['main_inca'] = same_helper.getMainIncaQhawaxTable(data['qhawax_id'])
            data['instalation_date_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            data['last_time_physically_turn_on_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            data['last_registration_time_zone'] = datetime.datetime.now(dateutil.tz.tzutc())
            qhawax_installation = QhawaxInstallationHistory(**data)
            session.add(qhawax_installation)
            session.commit()
        else:
            raise Exception("qHAWAX Installation fields have to have data")
    else:
        raise TypeError("The Json company "+str(data)+" should be in Json Format")


def writeBinnacle(qhawax_name,description,person_in_charge):
    """
    Write Binnacle

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type observation_type: string
    :param observation_type: Observation type

    :type description: string
    :param description: Bitacora description

    :type person_in_charge: string
    :param person_in_charge: Person in Charge

    """
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    bitacora = {'timestamp_zone': datetime.datetime.now(dateutil.tz.tzutc()), \
                'observation_type': 'Interna','description': description,  \
                'qhawax_id':qhawax_id,'solution':None,'person_in_charge':person_in_charge, \
                'end_date_zone':None,'start_date_zone':None}
    bitacora_update = Bitacora(**bitacora)
    session.add(bitacora_update)
    session.commit()


