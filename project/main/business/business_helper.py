import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio
from passlib.hash import bcrypt
import random
import string

import project.database.utils as utils

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, Company, User, \
        AirQualityMeasurement, ProcessedMeasurement, ValidProcessedMeasurement

from project.database.utils import Location

var_gases=['CO','H2S','NO','NO2','O3','SO2']

session = db.session

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
        qhawax_list = session.query(Qhawax.id).filter_by(name=qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one()[0]

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
        qhawax_list = session.query(Qhawax.id).filter_by(name=qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one()[0]

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
        qhawax_list = session.query(Qhawax.id).filter_by(name=qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one()[0]

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
        qhawax_list = session.query(Qhawax.id).filter_by(name=qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one()[0]

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
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_id).one()[0]

    for sensor_type in controlled_offsets:
        session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).update(values=controlled_offsets[sensor_type])
    
    session.commit()

def updateNonControlledOffsetsFromProductID(qhawax_id, non_controlled_offsets):
    """
    Helper Gas Sensor function to save non controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type offsets: json
    :param offsets: Json of offset variable of qHAWAX

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_id).one()[0]

    for sensor_type in non_controlled_offsets:
        session.query(GasSensor).filter_by(qhawax_id=qhawax_id, type=sensor_type).update(values=non_controlled_offsets[sensor_type])
    
    session.commit()

def queryDBPROM(qhawax_name, sensor, initial_timestamp, final_timestamp):
    """
    Helper Gas Sensor function to save non controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type sensor: string
    :param sensor: sensor type ('CO', 'NO2','PM10','PM25','SO2','O3','H2S')

    :type initial_timestamp: timestamp
    :param initial_timestamp: initial search date

    :type final_timestamp: timestamp
    :param final_timestamp: last search date

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None
    
    if sensor == 'CO':
        datos = AirQualityMeasurement.CO
        hoursPerSensor = 8
    elif sensor == 'NO2':
        datos = AirQualityMeasurement.NO2
        hoursPerSensor = 1
    elif sensor == 'PM10':
        datos = AirQualityMeasurement.PM10
        hoursPerSensor = 24
    elif sensor == 'PM25':
        datos = AirQualityMeasurement.PM25
        hoursPerSensor = 24
    elif sensor == 'SO2':
        datos = AirQualityMeasurement.SO2
        hoursPerSensor = 24
    elif sensor == 'O3':
        datos = AirQualityMeasurement.O3
        hoursPerSensor = 8
    elif sensor == 'H2S':
        datos = AirQualityMeasurement.H2S
        hoursPerSensor = 24

    resultado=[]
    resultado = session.query(datos).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                      filter(AirQualityMeasurement.timestamp > initial_timestamp). \
                                      filter(AirQualityMeasurement.timestamp < final_timestamp). \
                                      order_by(AirQualityMeasurement.timestamp).all()
    sum = 0        

    if len(resultado) == 0 :
        return 0
    else :
        for i in range(len(resultado)):
            sum = sum + resultado[i][0]
        promf = sum /len(resultado)
        
    return promf

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


def getQhawaxLatestTimestamp(qhawax_name):
    if(isinstance(qhawax_name, str)):
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one().id
        qhawax_time = session.query(RawMeasurement.timestamp).filter_by(qhawax_id=qhawax_id).first()
        raw_measurement_timestamp=""
        if(qhawax_time!=None):
            raw_measurement_timestamp = session.query(RawMeasurement.timestamp).filter_by(qhawax_id=qhawax_id) \
                .order_by(RawMeasurement.id.desc()).first().timestamp
        return raw_measurement_timestamp
    else:
        raise TypeError("The qhawax name should be string")

def getQhawaxLatestTimestampProcessedMeasurement(qhawax_name):
    if(isinstance(qhawax_name, str)):
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one().id
        qhawax_time = session.query(ProcessedMeasurement.timestamp).filter_by(qhawax_id=qhawax_id).first()
        processed_measurement_timestamp=""
        if(qhawax_time!=None):
            processed_measurement_timestamp = session.query(ProcessedMeasurement.timestamp).filter_by(qhawax_id=qhawax_id) \
                .order_by(ProcessedMeasurement.timestamp.desc()).first().timestamp
        return processed_measurement_timestamp
    else:
        raise TypeError("The qhawax name should be string")

#def getQhawaxLatestCoordinatesFromName(session, qhawax_name):
#    return session.query(Qhawax._location).filter_by(name=qhawax_name).first()

def getQhawaxStatus(qhawax_name):
    if(isinstance(qhawax_name, str)):
        state = session.query(Qhawax.state).filter_by(name=qhawax_name).one()[0]
        return state
    else:
        raise TypeError("The qhawax name should be string")

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
            session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'main_inca': -1, 'last_registration_time':qhawax_lost_timestamp})
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
        installation_id = getInstallationId(qhawax_id)
        if(installation_id!=None):
            now = datetime.datetime.now()-datetime.timedelta(hours=5)
            session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'last_time_physically_turn_on': now.replace(tzinfo=None)})
            session.commit()

def getInstallationIdBaseName(qhawax_name):
    qhawax_id = session.query(Qhawax.id).filter(Qhawax.name == qhawax_name).one()
    installation_id = getInstallationId(qhawax_id)
    return installation_id


def getTimeQhawaxHistory(installation_id):
    values= session.query(QhawaxInstallationHistory.last_time_physically_turn_on, QhawaxInstallationHistory.last_registration_time).filter(QhawaxInstallationHistory.id == installation_id).first()
    if (values!=None):
        return values
    else:
        return None

def storeNewQhawaxInstallation(data):
    """
    Insert new qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(areFieldsValid(data)==True):
        main_inca = getMainIncaQhawaxTable(data['qhawax_id'])
        installation_data = {'lat': data['lat'], 'lon': data['lon'], 'instalation_date': str(dateutil.parser.parse(data['instalation_date']) - datetime.timedelta(hours=5)), 'link_report': data['link_report'], 
                 'observations': data['observations'], 'district': data['district'],'comercial_name': data['comercial_name'],'address':data['address'],
                 'company_id': data['company_id'],'eca_noise_id':data['eca_noise_id'], 'qhawax_id':data['qhawax_id'],'connection_type':data['connection_type'],
                 'index_type':data['index_type'],'measuring_height':data['measuring_height'], 'season':data['season'], 'last_time_physically_turn_on':data['instalation_date'],
                 'last_registration_time': data['instalation_date'], 'main_inca':main_inca, 'is_public':data['is_public'],'person_in_charge':data['person_in_charge']}
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
    session.query(QhawaxInstallationHistory).filter_by(id=installation_id).update(values={'end_date': end_date})
    session.commit()

def setAvailableQhawax(qhawax_id):
    """
    Update qhawax installation state in qHAWAX table

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'availability': 'Available'})
    session.commit()

def queryQhawaxInField():
    """
    Get All qHAWAXs in field

    No parameters required

    """
    sensors = (QhawaxInstallationHistory.id, QhawaxInstallationHistory.qhawax_id, QhawaxInstallationHistory.district,
             QhawaxInstallationHistory.comercial_name,QhawaxInstallationHistory.instalation_date,
            Company.name, QhawaxInstallationHistory.is_public)

    return session.query(*sensors).join(Company, QhawaxInstallationHistory.company_id == Company.id). \
                                   group_by(Company.id, QhawaxInstallationHistory.id). \
                                   filter(QhawaxInstallationHistory.end_date == None). \
                                   order_by(QhawaxInstallationHistory.instalation_date.desc()).all()

def queryQhawaxInFieldByCompany(company_id):
    """
    Get list of qHAWAXs in field filter by company ID

    If company_id is 0, the response will be all public qHAWAX
    If company_id is other valid number, the response will refer to the modules of that company

    :type  company_id: integer
    :param company_id: company ID

    """
    columns = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, QhawaxInstallationHistory.id, QhawaxInstallationHistory.qhawax_id,
        QhawaxInstallationHistory.eca_noise_id, QhawaxInstallationHistory.comercial_name, QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon, EcaNoise.area_name)
    
    if(int(company_id)==0): #Qhawax instalados publicos activos
        return session.query(*columns).join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                                      join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                                      group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                                      filter(QhawaxInstallationHistory.is_public== 'si'). \
                                       filter(QhawaxInstallationHistory.end_date == None). \
                                        order_by(Qhawax.id).all() 
    return session.query(*columns).join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                                   join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                                   group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                                   filter(QhawaxInstallationHistory.company_id == company_id). \
                                   filter(QhawaxInstallationHistory.end_date == None). \
                                   order_by(Qhawax.id).all() 

def getAllQhawaxDetail(qhawax_list):
    """
    Get list of qHAWAXs in field

    :type  qhawax_list: json array
    :param qhawax_list: qHAWAX list

    """
    for qhawax_detail in qhawax_list:
        qhawax_detail['qhawax_id'] = qhawax_detail['id']

        qhawax_detail['id'] = session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_detail['qhawax_id'],end_date=None).all()
        if(qhawax_detail['id'] == []):
            qhawax_detail['id'] = 0
        else: qhawax_detail['id'] = session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_detail['qhawax_id'],end_date=None).first()[0]
        
        qhawax_detail['eca_noise_id'] = session.query(QhawaxInstallationHistory.eca_noise_id).filter_by(id=qhawax_detail['id']).all()
        if(qhawax_detail['eca_noise_id'] == []):
            qhawax_detail['eca_noise_id'] = 0
        else: qhawax_detail['eca_noise_id'] = session.query(QhawaxInstallationHistory.eca_noise_id).filter_by(id=qhawax_detail['id']).first()[0]
        
        qhawax_detail['area_name'] = session.query(EcaNoise.area_name).filter_by(id=qhawax_detail['eca_noise_id']).all()
        if(qhawax_detail['area_name'] == []):
            qhawax_detail['area_name'] = "Zona No Definida"
        else: qhawax_detail['area_name'] = session.query(EcaNoise.area_name).filter_by(id=qhawax_detail['eca_noise_id']).first()[0]
        
        qhawax_detail['comercial_name']  = session.query(QhawaxInstallationHistory.comercial_name).filter_by(id=qhawax_detail['id']).all()
        if(qhawax_detail['comercial_name']  == []):
            qhawax_detail['comercial_name']  = "Qhawax en " + qhawax_detail['mode']
        else: qhawax_detail['comercial_name']  = session.query(QhawaxInstallationHistory.comercial_name).filter_by(id=qhawax_detail['id']).first()[0]
        
        qhawax_detail['lat']  = session.query(QhawaxInstallationHistory.lat).filter_by(id=qhawax_detail['id']).all()
        if(qhawax_detail['lat']  == []):
            qhawax_detail['lat']  = 0
        else: qhawax_detail['lat'] = session.query(QhawaxInstallationHistory.lat).filter_by(id=qhawax_detail['id']).first()[0]

        qhawax_detail['lon'] = session.query(QhawaxInstallationHistory.lon).filter_by(id=qhawax_detail['id']).all()
        if(qhawax_detail['lon']  == []):
            qhawax_detail['lon']  = 0
        else: qhawax_detail['lon'] = session.query(QhawaxInstallationHistory.lon).filter_by(id=qhawax_detail['id']).first()[0]

    return qhawax_list

def queryQhawaxRecord(qhawax_id):
    sensors = (QhawaxInstallationHistory.id, QhawaxInstallationHistory.comercial_name, 
               QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon,
               QhawaxInstallationHistory.address, QhawaxInstallationHistory.district,
               QhawaxInstallationHistory.instalation_date, QhawaxInstallationHistory.end_date)
    return session.query(*sensors).filter(QhawaxInstallationHistory.qhawax_id == qhawax_id). \
                                   order_by(QhawaxInstallationHistory.id.desc()).all()

def getInstallationDateByQhawaxID(qhawax_id):
    installation_date = session.query(QhawaxInstallationHistory.instalation_date).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date == None). \
                                    order_by(QhawaxInstallationHistory.instalation_date.desc()).first()
    if (installation_date==None):
        return installation_date
    return installation_date[0]

def getInstallationId(qhawax_id):
    installation_id= session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date == None). \
                                    order_by(QhawaxInstallationHistory.instalation_date.desc()).all()
    if(installation_id == []):
        return None

    return session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date == None). \
                                    order_by(QhawaxInstallationHistory.instalation_date.desc()).first()[0]

def getFirstTimestampValidProcessed(qhawax_installation_id):

    first_timestamp =session.query(ValidProcessedMeasurement.timestamp).filter(ValidProcessedMeasurement.qhawax_installation_id == int(qhawax_installation_id)). \
                                    order_by(ValidProcessedMeasurement.timestamp.asc()).first()                  
    if (first_timestamp==None):
        return first_timestamp
    return first_timestamp[0]

def queryDateOfActiveQhawax():
    sensors = (QhawaxInstallationHistory.id,QhawaxInstallationHistory.instalation_date, QhawaxInstallationHistory.end_date,
               QhawaxInstallationHistory.last_maintenance_date, QhawaxInstallationHistory.last_cleaning_area_date ,
               QhawaxInstallationHistory.last_cleaning_equipment_date,QhawaxInstallationHistory.qhawax_id,
               QhawaxInstallationHistory.comercial_name, QhawaxInstallationHistory.company_id)
    return session.query(*sensors).filter(QhawaxInstallationHistory.end_date == None).all()

def queryQhawaxInstallationDetail(installation_id):
    sensors = (QhawaxInstallationHistory.id, QhawaxInstallationHistory.comercial_name, 
               QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon,
               QhawaxInstallationHistory.address, QhawaxInstallationHistory.district,
               QhawaxInstallationHistory.instalation_date, QhawaxInstallationHistory.end_date,
               QhawaxInstallationHistory.link_report,QhawaxInstallationHistory.qhawax_id,
               QhawaxInstallationHistory.connection_type, QhawaxInstallationHistory.index_type, 
               QhawaxInstallationHistory.measuring_height, QhawaxInstallationHistory.season,
               QhawaxInstallationHistory.last_maintenance_date, QhawaxInstallationHistory.last_cleaning_area_date ,
               QhawaxInstallationHistory.last_cleaning_equipment_date, QhawaxInstallationHistory.person_in_charge)
    return session.query(*sensors).filter(QhawaxInstallationHistory.id == installation_id).all()


def getMainIncaQhawax(name):
    installation_id=getInstallationIdBaseName(name)
    qhawax_inca = session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).one()[0]
    return qhawax_inca

def updateCompany(company_id, email):
    session.query(User).filter_by(email=email).update(values={'company_id': company_id})
    session.commit()

def queryUsersCompany():
    sensors = (User.company_id, User.email)
    user_list = session.query(*sensors).order_by(User.company_id).all()
    return user_list

def changePassword(user, new_pass_decoded):
    if(user!='' and new_pass_decoded!=''):
        if(isinstance(user, User) and isinstance(new_pass_decoded, str)):
            user.changePassword(new_pass_decoded)
            session.commit()
        else:
            raise TypeError("The user and password are not in the correct way")
    else:
        raise TypeError("The user or password are empty")

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

def createUser(email,company_id,company_name, email_group, password):
    """
    Create User

    :type email: string
    :param email: user email

    :type company_id: integer
    :param company_id: company ID

    :type company_name: string
    :param company_name: user company name

    :type email_group: string
    :param email_group: company email group

    :type password: string
    :param password: user password

    """
    if(isinstance(email, str) and isinstance(password, str)):
        utils.checkPasswordLength(password)
        utils.checkEmailIsFromCompany(email, company_name, email_group)
        password_hash = bcrypt.encrypt(password)
        user_data = {'company_id': company_id, 'email': email, 'password_hash':password_hash}
        user = User(**user_data)
        session.add(user)
        session.commit()
    else:
        raise TypeError("The email and password should be string")


def getCompany(company_id):
    """
    Get company object base on company ID

    :type company_id: integer
    :param company_id: company ID

    """
    if(type(company_id) not in [int]):
        raise TypeError("The company id should be int")
    sensors = (Company.name, Company.email_group)
    company = session.query(*sensors).filter_by(id=company_id).first()
    return company

def getQhawaxId(qhawax_name):
    """
    Get qHAWAX ID base on qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    return qhawax_id

def randomString(stringLength=10):
    """
    Get random string

    :type stringLength: integer
    :param stringLength: number of characters

    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def queryQhawaxModeCustomer():
    """
    Get qHAWAX list in mode Customer and state ON

    No parameters required

    """
    qhawax_column = (Qhawax.id, Qhawax.name, Qhawax.main_inca, Qhawax.qhawax_type)
    qhawax_list = session.query(*qhawax_column).filter_by(mode="Cliente",state="ON").order_by(Qhawax.id).all()
    return qhawax_list

def getDescriptionOfQhawaxInField(qhawax_in_customer_mode):
    """
    Get comercial description of qHAWAX in field

    :type qhawax_in_customer_mode: json
    :param qhawax_in_customer_mode: json of qHAWAX detail in mode customer

    """
    for qhawax in qhawax_in_customer_mode:
        qhawax['comercial_name']= session.query(QhawaxInstallationHistory.comercial_name).filter_by(qhawax_id=qhawax['id'],end_date=None).all()
        if(qhawax['comercial_name'] == []):
            raise TypeError("The qHAWAXs selected are not in field, they have end date of work")
        qhawax['comercial_name'] = session.query(QhawaxInstallationHistory.comercial_name).filter_by(qhawax_id=qhawax['id'],end_date=None).first()[0]
        qhawax['eca_noise_id']= session.query(QhawaxInstallationHistory.eca_noise_id).filter_by(qhawax_id=qhawax['id'],end_date=None).first()[0]

    return qhawax_in_customer_mode

def setModeCustomer(qhawax_id):
    """
    Update qHAWAX mode to Customer

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    session.query(Qhawax).filter_by(id=qhawax_id).update(values={'mode': "Cliente"})
    session.commit()

def getMainIncaQhawaxTable(qhawax_id):
    """
    Get qHAWAX Main Inca

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    main_inca = session.query(Qhawax.main_inca).filter_by(id=qhawax_id).one()[0]
    return main_inca

def queryAllQhawax():
    """
    Get all qHAWAXs

    No parameters required

    """
    columns = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, Qhawax.id)
    return session.query(*columns).order_by(Qhawax.id).all()

def queryAllQhawaxByMode(qhawax_mode):
    """
    Get all qHAWAXs

    :type qhawax_mode: string
    :param qhawax_mode: qHAWAX mode

    """
    columns = (Qhawax.name, Qhawax.id)
    return session.query(*columns).filter_by(mode=qhawax_mode).order_by(Qhawax.id).all()

def queryLastQhawax():
    """
    Get last qHAWAX

    No parameters required

    """
    columns = (Qhawax.name, Qhawax.id)
    return session.query(*columns).order_by(Qhawax.id.desc()).limit(1).all()


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

def setEmailBody(secret_key_hashed, subject, content1, content2):
    """
    Set Email Body and then send email

    :type secret_key_hashed: string
    :param secret_key_hashed: secret key

    :type subject: string
    :param subject: subject

    :type content1: string
    :param content1: content first part

    :type content2: string
    :param content2: content second part

    """
    if bcrypt.verify(app.config['SECRET_KEY'], str(secret_key_hashed)):
        content = content1 + content2
        sendEmail(to=app.config['MAIL_DEFAULT_RECEIVER'], subject=subject, template=content)
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

def setQhawaxName(qhawax_in_field_list):
    """
    Get qhawax name in this json list

    :type qhawax_in_field_list: json
    :param qhawax_in_field_list: json of qHAWAX detail in mode customer

    """
    for qhawax in qhawax_in_field_list:
        qhawax['qhawax_name']= session.query(Qhawax.name).filter_by(id=qhawax['qhawax_id']).one()[0]

    return qhawax_in_field_list


def writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date):
    """
    Write Bitacora

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type observation_type: string
    :param observation_type: Observation type

    :type description: string
    :param description: Bitacora description

    :type solution: string
    :param solution: Bitacora Solution

    :type person_in_charge: string
    :param person_in_charge: Person in Charge

    :type end_date: string
    :param end_date: End date

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    bitacora = {'timestamp': datetime.datetime.now()-datetime.timedelta(hours=5),'observation_type': observation_type,'description': description, 'qhawax_id':qhawax_id,'solution':solution,'person_in_charge':person_in_charge,'end_date':end_date}
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


def getQhawaxName(qhawax_id):
    """
    Get qHAWAX Name

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    return session.query(Qhawax.name).filter(Qhawax.id == qhawax_id).one()   


def areFieldsValid(data):
    if(data['lat']=='' or data['lat']==None):
        return False

    if(data['lon']=='' or data['lon']==None):
        return False

    if(data['comercial_name']=='' or data['comercial_name']==None):
        return False

    if(data['company_id']=='' or data['company_id']==None):
        return False

    if(data['eca_noise_id']=='' or data['eca_noise_id']==None):
        return False

    if(data['qhawax_id']=='' or data['qhawax_id']==None):
        return False

    if(data['connection_type']=='' or data['connection_type']==None):
        return False

    if(data['season']=='' or data['season']==None):
        return False

    if(data['is_public']=='' or data['is_public']==None):
        return False

    if(data['person_in_charge']=='' or data['person_in_charge']==None):
        return False

    return True

def updateQhawaxInstallation(data):
    """
    Update qHAWAX in Field 

    :type data: json
    :param data: qHAWAX Installation detail

    """
    if(areFieldsValid(data)==True):
        session.query(QhawaxInstallationHistory).filter_by(qhawax_id=data['qhawax_id'],company_id=data['company_id'],end_date=None).update(values={'lat':data['lat'],'lon':data['lon'],'link_report': data['link_report'], 
                 'observations':data['observations'],'district':data['district'],'comercial_name':data['comercial_name'],'address':data['address'],'eca_noise_id':data['eca_noise_id'],'connection_type':data['connection_type'],
                 'measuring_height':data['measuring_height'],'season':data['season'], 'is_public':data['is_public'],'person_in_charge':data['person_in_charge']})
        session.commit()
    else:
        raise Exception("The qhawax installation fields have to have data")

def queryAllObservationByQhawax(qhawax_id):
    """
    Get all qHAWAXs observation

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    columns = (Bitacora.id, Bitacora.timestamp, Bitacora.observation_type,Bitacora.description, Bitacora.solution, Bitacora.person_in_charge, Bitacora.end_date)
    return session.query(*columns).filter_by(qhawax_id=qhawax_id).order_by(Bitacora.timestamp).all()

def storeNewObservation(data):
    """
    Binnacle helper function to record observations in field
    
    Json input of following fields:
    
    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type initial_timestamp: timestamp
    :param initial_timestamp: start observation

    :type end_timestamp: timestamp
    :param end_timestamp: end observation

    :type description: string
    :param description: description of the observation

    :type solution: string
    :param solution: solution of the observation

    :type person_in_charge: string
    :param person_in_charge: person in charge
    """
    qhawax_mode = session.query(Qhawax.mode).filter_by(id=data['qhawax_id']).one()[0]
    if(qhawax_mode=='Cliente'):
        observation = {'qhawax_id': data['qhawax_id'], 'timestamp': data['initial_timestamp'], 'end_date': data['end_timestamp'], 
                     'description': data['description'], 'solution': data['solution'],'person_in_charge': data['person_in_charge'],'observation_type':'Externa'}
        binnacle_observation = Bitacora(**observation)
        session.add(binnacle_observation)
        session.commit()

