import time
from project import app, db
import string
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, AirQualityMeasurement, ProcessedMeasurement, \
                                    ValidProcessedMeasurement
session = db.session

def getTimeQhawaxHistory(installation_id):
    """
    Get time qHAWAX History

    :type installation_id: integer
    :param installation_id: Installation ID

    """
    fields = (QhawaxInstallationHistory.last_time_physically_turn_on_zone,\
              QhawaxInstallationHistory.last_registration_time_zone)
    if(same_helper.verifyIfQhawaxInstallationExistBaseOnID(installation_id)==True):
        values = session.query(*fields).filter_by(id= installation_id).first()
        return values

def queryQhawaxModeCustomer():
    """
    Get qHAWAX list in mode Customer and state ON

    No parameters required

    """
    qhawax_column = (Qhawax.id, Qhawax.name, Qhawax.main_inca, Qhawax.qhawax_type,\
                     QhawaxInstallationHistory.comercial_name, EcaNoise.area_name)

    qhawax_list = session.query(*qhawax_column).\
                          join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                          join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                          group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                          filter(Qhawax.mode =="Cliente", \
                                 Qhawax.state =="ON", \
                                 QhawaxInstallationHistory.end_date_zone == None).order_by(Qhawax.id).all()
    return qhawax_list

def queryGetAreas():
    """
    Helper Eca Noise function to list all zones 

    No parameters required

    """
    fields = (EcaNoise.id, EcaNoise.area_name)
    areas = session.query(*fields).all()
    if(areas == []):
        return None
    return session.query(*fields).order_by(EcaNoise.id.desc()).all()

def queryGetEcaNoise(eca_noise_id):
    """
    Helper Eca Noise function to get zone description

    :type eca_noise_id: integer
    :param eca_noise_id: Eca Noise ID

    """
    fields = (EcaNoise.id, EcaNoise.area_name, EcaNoise.max_daytime_limit, \
              EcaNoise.max_night_limit)
    if(same_helper.verifyIfAreaExistBaseOnID(eca_noise_id)==True):
        return session.query(*fields).filter_by(id= eca_noise_id).first()


def getOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.WE, GasSensor.AE, \
                  GasSensor.sensitivity, GasSensor.sensitivity_2)
    if(isinstance(qhawax_name, str)):
        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        offsets_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        
        offset_json = {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}
        initial_offset_json = util_helper.initializeOffsetJson(offset_json)

        for sensor in offsets_sensors:
            sensor_dict = sensor._asdict()
            initial_offset_json[sensor_dict.pop('type')] = sensor_dict

        return initial_offset_json
    else:
        raise TypeError("The qHAWAX name should be string")


def getControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.C2, GasSensor.C1, GasSensor.C0)
    if(isinstance(qhawax_name, str)):
        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        controlled_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()

        controlled_offset_json = {'C0': 0.0, 'C1': 0.0, 'C2': 0.0}
        initial_controlled_offsets = util_helper.initializeOffsetJson(controlled_offset_json)

        for sensor in controlled_sensors:
            sensor_dict = sensor._asdict()
            initial_controlled_offsets[sensor_dict.pop('type')] = sensor_dict
        
        return initial_controlled_offsets
    else:
        raise TypeError("The qHAWAX name should be string")

def getNonControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get non controlled offsets from qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.NC1, GasSensor.NC0)
    if(isinstance(qhawax_name, str)):
        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        non_controlled_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()

        non_controlled_offsets = {'NC1': 0.0, 'NC0': 0.0}
        initial_non_controlled_offsets = util_helper.initializeOffsetJson(non_controlled_offsets)

        for sensor in non_controlled_sensors:
            sensor_dict = sensor._asdict()
            initial_non_controlled_offsets[sensor_dict.pop('type')] = sensor_dict
        return initial_non_controlled_offsets
    else:
        raise TypeError("The qHAWAX name should be string")


def queryIncaQhawax(name):
    """
    Helper qHAWAX function to get main inca value

    :type name: string
    :param name: qHAWAX name

    """
    if(isinstance(name, str)):
        qhawax_id = same_helper.getQhawaxID(name)
        qhawax_inca = same_helper.getMainIncaQhawaxTable(qhawax_id)
        return util_helper.getColorBaseOnIncaValue(qhawax_inca)
    else:
        raise TypeError("The qHAWAX name should be string")

def getInstallationDateByQhawaxID(qhawax_id):
    installation_date = session.query(QhawaxInstallationHistory.installation_date_zone).\
                                filter_by(qhawax_id=qhawax_id). \
                                filter(QhawaxInstallationHistory.end_date_zone == None). \
                                order_by(QhawaxInstallationHistory.installation_date_zone.desc()).first()[0]
    if (installation_date==None):
        return installation_date
    return installation_date[0]

def getFirstTimestampValidProcessed(qhawax_installation_id):

    first_timestamp =session.query(ValidProcessedMeasurement.timestamp_zone). \
                             filter(ValidProcessedMeasurement.qhawax_installation_id == int(qhawax_installation_id)). \
                             order_by(ValidProcessedMeasurement.timestamp_zone.asc()).first()[0]               
    if (first_timestamp==None):
        return first_timestamp
    return first_timestamp[0]

def getMainIncaQhawax(name):
    installation_id=same_helper.getInstallationIdBaseName(name)
    qhawax_inca = session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).first()[0]
    return qhawax_inca

def queryGetLastQhawax():
    qhawax_list = session.query(Qhawax.id).all()
    if(qhawax_list==[]):
        return None

    return session.query(Qhawax.id).order_by(Qhawax.id.desc()).all()[0]

def queryGetLastGasSensor():
    gas_sensor_list = session.query(GasSensor.id).all()
    if(gas_sensor_list==[]):
        return None

    return session.query(GasSensor.id).order_by(GasSensor.id.desc()).all()[0]


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

def isItFieldQhawax(qhawax_name):
    """
    Check qhawax in field

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id != None):
        return True
    return False

def getQhawaxLatestTimestampProcessedMeasurement(qhawax_name):
    """
    Helper qHAWAX function to get latest timestamp in UTC 00 from Processed Measurement
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name
    
    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        qhawax_time = session.query(ProcessedMeasurement.timestamp_zone).\
                              filter_by(qhawax_id=qhawax_id).first()[0]
        processed_measurement_timestamp=""
        if(qhawax_time!=None):
            processed_measurement_timestamp = session.query(ProcessedMeasurement.timestamp_zone).\
                                                      filter_by(qhawax_id=qhawax_id).\
                                                      order_by(ProcessedMeasurement.id.desc()).first().timestamp_zone
        return processed_measurement_timestamp
    else:
        raise TypeError("The qHAWAX name should be string")


def getQhawaxLatestTimestampValidProcessedMeasurement(qhawax_name):
    """
    Helper qHAWAX function to get latest timestamp in UTC 00 from Valid Processed Measurement
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name
    
    """
    if(isinstance(qhawax_name, str)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        valid_processed_measurement_timestamp=""
        if(installation_id != None):
            qhawax_time = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                  filter_by(qhawax_installation_id=installation_id).first()[0]
            if(qhawax_time!=None):
                valid_processed_measurement_timestamp = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                                                filter_by(qhawax_installation_id=installation_id) \
                                                                .order_by(ValidProcessedMeasurement.timestamp_zone.desc()).first().timestamp_zone
        
        return valid_processed_measurement_timestamp
    else:
        raise TypeError("The qHAWAX name should be string")

def queryQhawaxInFieldInPublicMode():
    """
    Get list of qHAWAXs in field in public mode
    
    No parameters required

    """
    columns = (Qhawax.name, Qhawax.mode,Qhawax.state,Qhawax.qhawax_type,Qhawax.main_inca, 
               QhawaxInstallationHistory.id, QhawaxInstallationHistory.qhawax_id,
               QhawaxInstallationHistory.eca_noise_id, QhawaxInstallationHistory.comercial_name, 
               QhawaxInstallationHistory.lat, QhawaxInstallationHistory.lon, EcaNoise.area_name)
    
    return session.query(*columns).join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                                   join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                                   group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                                   filter(QhawaxInstallationHistory.is_public == 'si'). \
                                   filter(QhawaxInstallationHistory.end_date_zone == None). \
                                   order_by(Qhawax.id).all() 

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
                                      filter(AirQualityMeasurement.timestamp_zone > initial_timestamp). \
                                      filter(AirQualityMeasurement.timestamp_zone < final_timestamp). \
                                      order_by(AirQualityMeasurement.timestamp_zone).all()
    sum = 0        

    if len(resultado) == 0 :
        return 0
    else :
        for i in range(len(resultado)):
            sum = sum + resultado[i][0]
        promf = sum /len(resultado)
        
    return promf
