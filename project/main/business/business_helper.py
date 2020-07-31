import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio
from passlib.hash import bcrypt
import random
import string

import project.database.utils as utils
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, Company, AirQualityMeasurement, ProcessedMeasurement, ValidProcessedMeasurement, Bitacora

var_gases=['CO','H2S','NO','NO2','O3','SO2']

session = db.session


def getInstallationIdBaseName(qhawax_name):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    installation_id = same_helper.getInstallationId(qhawax_id)
    return installation_id

def getMainIncaQhawaxTable(qhawax_id):
    """
    Get qHAWAX Main Inca

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    main_inca = session.query(Qhawax.main_inca).filter_by(id=qhawax_id).one()[0]
    return main_inca

def queryGetCompanies():
    """
    Helper Company function to list all companies 

    No parameters required

    """
    sensors = (Company.id, Company.name, Company.email_group, Company.ruc, Company.address, Company.phone, Company.contact_person)
    companies = session.query(*sensors).all()
    if(companies == []):
        return None
    return session.query(*sensors).order_by(Company.id.desc()).all()

def queryGetEcaNoise(eca_noise_id):
    """
    Helper Eca Noise function to get zone description

    :type eca_noise_id: integer
    :param eca_noise_id: Eca Noise ID

    """
    if(type(eca_noise_id) not in [int]):
        raise TypeError("The eca noise id should be int")
    fields = (EcaNoise.id, EcaNoise.area_name, EcaNoise.max_daytime_limit, EcaNoise.max_night_limit)
    area_list = session.query(*fields).filter(EcaNoise.id == eca_noise_id).all()
    if (area_list == []):
        return area_list
    return session.query(*fields).filter(EcaNoise.id == eca_noise_id).one()

def queryGetAreas():
    """
    Helper Eca Noise function to list all zones 

    No parameters required

    """
    sensors = (EcaNoise.id, EcaNoise.area_name)
    return session.query(*sensors).order_by(EcaNoise.id.desc()).all()


def getOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        attributes = (GasSensor.type, GasSensor.WE, GasSensor.AE, GasSensor.sensitivity, GasSensor.sensitivity_2)
        sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        all_sensors=['CO','SO2','H2S','O3','NO','NO2']

        initial_offsets = {}
        for sensor in all_sensors:
            initial_offsets[sensor] = {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}

        for sensor in sensors:
            sensor_dict = sensor._asdict()
            initial_offsets[sensor_dict.pop('type')] = sensor_dict

        return initial_offsets
    else:
        raise TypeError("The qHAWAX name should be string")

def getControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        attributes = (GasSensor.type, GasSensor.C2, GasSensor.C1, GasSensor.C0)
        sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        all_sensors=['CO','SO2','H2S','O3','NO','NO2']

        initial_offsets = {}
        for sensor in all_sensors:
            initial_offsets[sensor] = {'C0': 0.0, 'C1': 0.0, 'C2': 0.0}

        for sensor in sensors:
            sensor_dict = sensor._asdict()
            initial_offsets[sensor_dict.pop('type')] = sensor_dict
        
        return initial_offsets
    else:
        raise TypeError("The qHAWAX name should be string")


def getNonControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get non controlled offsets from qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        attributes = (GasSensor.type, GasSensor.NC1, GasSensor.NC0)
        sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        all_sensors=['CO','SO2','H2S','O3','NO','NO2']

        initial_offsets = {}
        for sensor in all_sensors:
            initial_offsets[sensor] = {'NC1': 0.0, 'NC0': 0.0}

        for sensor in sensors:
            sensor_dict = sensor._asdict()
            initial_offsets[sensor_dict.pop('type')] = sensor_dict
        return initial_offsets
    else:
        raise TypeError("The qHAWAX name should be string")

def updateOffsetsFromProductID(qhawax_name, offsets):
    """
    Helper Gas Sensor function to save offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        for sensor_type in offsets:
            session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).update(values=offsets[sensor_type])

        session.commit()
    else:
        raise TypeError("The qHAWAX name should be string")


def updateControlledOffsetsFromProductID(qhawax_id, controlled_offsets):
    """
    Helper Gas Sensor function to save controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        for sensor_type in controlled_offsets:
            session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).update(values=controlled_offsets[sensor_type])
    
        session.commit()
    else:
        raise TypeError("The qHAWAX name should be string")


def updateNonControlledOffsetsFromProductID(qhawax_id, non_controlled_offsets):
    """
    Helper Gas Sensor function to save non controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = getQhawaxID(qhawax_name)

        for sensor_type in non_controlled_offsets:
            session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).update(values=non_controlled_offsets[sensor_type])
    
        session.commit()
    else:
        raise TypeError("The qHAWAX name should be string")

def queryIncaQhawax(name):
    """
    Helper qHAWAX function to get main inca value

    :type name: string
    :param name: qHAWAX name

    """
    if(isinstance(name, str)):
        qhawax_inca = session.query(Qhawax.main_inca).filter_by(name=name).one()
        if qhawax_inca[0] == 50:
            resultado = 'green'
        elif qhawax_inca[0] == 100:
            resultado = 'yellow'
        elif qhawax_inca[0] == 500:
            resultado = 'orange'
        elif qhawax_inca[0] == 600:
            resultado = 'red'
        else:
            resultado = 'green'
        return resultado
    else:
        raise TypeError("The qhawax name should be string")


def updateMainIncaInDB(new_main_inca, qhawax_name):
    """
    Helper qHAWAX function to save main inca value in qHAWAX and qHAWAX Installation table

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type new_main_inca: integer
    :param new_main_inca: qHAWAX main inca

    """
    jsonsend = {}
    session.query(Qhawax).filter_by(name=qhawax_name).update(values={'main_inca': new_main_inca})
    session.commit()
    qhawax_mode = session.query(Qhawax.mode).filter_by(name=qhawax_name).one()[0]
    if(qhawax_mode=='Cliente'):
        installation_id=getInstallationIdBaseName(qhawax_name)
        session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'main_inca': new_main_inca})
        session.commit()
    jsonsend['main_inca'] = new_main_inca
    jsonsend['name'] = qhawax_name 
    socketio.emit('update_inca', jsonsend)

def saveStatusOff(json):
    jsonsend={}
    qhawax_name = str(json['qhawax_name']).strip()
    qhawax_lost_timestamp = dateutil.parser.parse(str(json['qhawax_lost_timestamp']).strip()) #falta verificar que sea formato fecha
    if(isinstance(qhawax_name, str)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'state': "OFF",'main_inca':-1})
        session.commit()
        qhawax_mode = session.query(Qhawax.mode).filter_by(name=qhawax_name).one()[0]
        if(qhawax_mode=='Cliente'):
            installation_id=getInstallationIdBaseName(qhawax_name)
            session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'main_inca': -1, 'last_registration_time_zone':qhawax_lost_timestamp})
            session.commit()
        jsonsend['main_inca'] = -1
        jsonsend['name'] = qhawax_name 
        socketio.emit('update_inca', jsonsend)
    else:
        raise TypeError("The qhawax name should be string")

def saveStatusOn(qhawax_name):
    if(isinstance(qhawax_name, str)):
        session.query(Qhawax).filter_by(name=qhawax_name).update(values={'state': "ON"})
        session.commit()
    else:
        raise TypeError("The qhawax name should be string")

def saveTurnOnLastTime(qhawax_name):
    qhawax_id, mode = session.query(Qhawax.id, Qhawax.mode).filter_by(name=qhawax_name).first()
    if(mode=='Cliente'):
        installation_id = same_helper.getInstallationId(qhawax_id)
        if(installation_id!=None):
            now = datetime.datetime.now(dateutil.tz.tzutc())
            session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'last_time_physically_turn_on_zone': now.replace(tzinfo=None)})
            session.commit()

def storeNewQhawaxInstallation(data):
    """
    Insert new qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(util_helper.areFieldsValid(data)==True):
        main_inca = getMainIncaQhawaxTable(data['qhawax_id'])
        installation_data = {'lat': data['lat'], 'lon': data['lon'], 'instalation_date_zone': datetime.datetime.now(dateutil.tz.tzutc()), 'link_report': data['link_report'], 
                 'observations': data['observations'], 'district': data['district'],'comercial_name': data['comercial_name'],'address':data['address'],
                 'company_id': data['company_id'],'eca_noise_id':data['eca_noise_id'], 'qhawax_id':data['qhawax_id'],'connection_type':data['connection_type'],
                 'index_type':data['index_type'],'measuring_height':data['measuring_height'], 'season':data['season'], 'last_time_physically_turn_on_zone':datetime.datetime.now(dateutil.tz.tzutc()),
                 'last_registration_time_zone': datetime.datetime.now(dateutil.tz.tzutc()), 'main_inca':main_inca, 'is_public':data['is_public'],'person_in_charge':data['person_in_charge']}
        qhawax_installation = QhawaxInstallationHistory(**installation_data)
        session.add(qhawax_installation)
        session.commit()
    else:
        raise Exception("The qhawax installation fields have to have data")


def setOccupiedQhawax(qhawax_id):
    """
    Update qHAWAX Availability to Occupied

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Occupied'})
    session.commit()

def saveEndWorkFieldDate(installation_id,end_date):
    """
    Save End Work in Field

    :type installation_id: integer
    :param installation_id: qHAWAX installation ID

    :type end_date: timestamp
    :param end_date: qHAWAX installation end date

    """
    session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'end_date_zone': end_date})
    session.commit()

def setAvailableQhawax(qhawax_id):
    """
    Update qhawax installation state in qHAWAX table

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Available'})
    session.commit()


def getInstallationDateByQhawaxID(qhawax_id):
    installation_date = session.query(QhawaxInstallationHistory.instalation_date).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date_zone == None). \
                                    order_by(QhawaxInstallationHistory.instalation_date_zone.desc()).first()
    if (installation_date==None):
        return installation_date
    return installation_date[0]


def getFirstTimestampValidProcessed(qhawax_installation_id):

    first_timestamp =session.query(ValidProcessedMeasurement.timestamp).filter(ValidProcessedMeasurement.qhawax_installation_id == int(qhawax_installation_id)). \
                                    order_by(ValidProcessedMeasurement.timestamp.asc()).first()                  
    if (first_timestamp==None):
        return first_timestamp
    return first_timestamp[0]

def getMainIncaQhawax(name):
    installation_id=getInstallationIdBaseName(name)
    qhawax_inca = session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).one()[0]
    return qhawax_inca

def queryGetLastQhawax():
    qhawax_list = session.query(Qhawax.id).all()
    if(qhawax_list==[]):
        return None

    return session.query(Qhawax.id).order_by(Qhawax.id.desc()).all()[0]

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
        raise TypeError("The qhawax id should be int")
    
    if(isinstance(qhawax_name, str) and isinstance(qhawax_type, str)):
        qhawax_data = {'id':qhawax_id,'name': qhawax_name, 'qhawax_type': qhawax_type,'state': 'OFF', 'availability': "Available", 'main_inca':-1.0, 'main_aqi':-1.0,'mode':"Stand By"}
        qhawax_data_var = Qhawax(**qhawax_data)
        session.add(qhawax_data_var)
        session.commit()
    else:
        raise TypeError("The qhawax name and type should be string")

def queryGetLastGasSensor():
    gas_sensor_list = session.query(GasSensor.id).all()
    if(gas_sensor_list==[]):
        return None

    return session.query(GasSensor.id).order_by(GasSensor.id.desc()).all()[0]

def insertDefaultOffsets(last_gas_sensor_id, qhawax_name):
    """
    To insert a Default Offset 
    
    :type last_gas_sensor_id: integer
    :param last_gas_sensor_id: last gas sensor ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one()[0]
    initial_serial_number = int(qhawax_id)*100
    start = 1
    for index in range(len(var_gases)):
        sensor_data = {'id':int(last_gas_sensor_id)+start,'serial_number': initial_serial_number + start, 'type': var_gases[index],'WE': 0.0, 'AE': 0.0,'sensitivity': 0.0, 'sensitivity_2': 0.0,'qhawax_id':qhawax_id, 'C0':0.0,'C1':0.0,'C2':0.0,'NC0':0.0,'NC1':0.0}
        sensor_data_var = GasSensor(**sensor_data)
        session.add(sensor_data_var)
        session.commit()
        start+=1

def createCompany(json):   
    company_data = {'name': json['company_name'], 'email_group': json['email_group'],'ruc':json['ruc'],'address':json['address'],'contact_person':json['contact_person'],'phone':json['phone']}
    company_var = Company(**company_data)
    session.add(company_var)
    session.commit()


def setModeCustomer(qhawax_id):
    """
    Update qHAWAX mode to Customer

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'mode': "Cliente"})
    session.commit()

def qhawaxNameIsNew(name):
    """
    Get True or False if qHAWAX name already exist

    :type name: string
    :param name: qHAWAX name

    """
    name = session.query(Qhawax.name).filter_by(name=name).all()
    if (name == []):
        return True
    return False

def companyNameIsNew(name):
    """
    Get True or False if company name already exist

    :type name: string
    :param name: company name

    """
    name = session.query(Company.name).filter_by(name=name).all()
    if (name == []):
        return True
    return False

def companyRucIsNew(ruc):
    """
    Get True or False if ruc already exist

    :type ruc: string
    :param ruc: RUC of company

    """
    ruc = session.query(Company.ruc).filter_by(ruc=ruc).all()
    if (ruc == []):
        return True
    return False

def changeMode(qhawax_name, mode):
    """
    Change To Other Mode

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    session.query(Qhawax).filter_by(name=qhawax_name).update(values={'mode': mode})
    session.commit()


def writeBitacora(qhawax_id,observation_type,description,person_in_charge):
    """
    Write Bitacora

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type observation_type: string
    :param observation_type: Observation type

    :type description: string
    :param description: Bitacora description

    :type person_in_charge: string
    :param person_in_charge: Person in Charge

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    bitacora = {'timestamp': datetime.datetime.now(dateutil.tz.tzutc()),'observation_type': observation_type,'description': description, 'qhawax_id':qhawax_id,'solution':None,'person_in_charge':person_in_charge,'end_date':None,'start_date':None}
    bitacora_update = Bitacora(**bitacora)
    session.add(bitacora_update)
    session.commit()


def isItFieldQhawax(qhawax_name):
    """
    Check qhawax in field

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    installation_id=getInstallationIdBaseName(qhawax_name)
    if(installation_id != None):
        return True
    return False


def updateQhawaxInstallation(data):
    """
    Update qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(util_helper.areFieldsValid(data)==True):
        session.query(QhawaxInstallationHistory).filter_by(qhawax_id=data['qhawax_id'],company_id=data['company_id'],end_date=None).update(values={'lat':data['lat'],'lon':data['lon'],'link_report': data['link_report'], 
                 'observations':data['observations'],'district':data['district'],'comercial_name':data['comercial_name'],'address':data['address'],'eca_noise_id':data['eca_noise_id'],'connection_type':data['connection_type'],
                 'measuring_height':data['measuring_height'],'season':data['season'], 'is_public':data['is_public'],'person_in_charge':data['person_in_charge']})
        session.commit()
    else:
        raise Exception("The qhawax installation fields have to have data")

def queryAllQhawax():
    """
    Get all qHAWAXs

    No parameters required

    """
    columns = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, Qhawax.id)
    return session.query(*columns).order_by(Qhawax.id).all()


def queryQhawaxInFieldByCompanyInPublicMode(company_id):
    """
    Get list of qHAWAXs in field filter by company ID

    Filter by COMPANY ID, the response will refer to the modules of that company

    :type  company_id: integer
    :param company_id: company ID

    """
    columns = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, QhawaxInstallationHistory.id, QhawaxInstallationHistory.qhawax_id,
        QhawaxInstallationHistory.eca_noise_id, QhawaxInstallationHistory.comercial_name, QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon, EcaNoise.area_name)
    
    return session.query(*columns).join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                                   join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                                   group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                                   filter(QhawaxInstallationHistory.is_public == 'si'). \
                                   filter(QhawaxInstallationHistory.company_id == company_id). \
                                   filter(QhawaxInstallationHistory.end_date == None). \
                                   order_by(Qhawax.id).all() 

