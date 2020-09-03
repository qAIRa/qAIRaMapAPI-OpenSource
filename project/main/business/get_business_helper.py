import time
from project import app, db
import string
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, AirQualityMeasurement, ProcessedMeasurement, \
                                    ValidProcessedMeasurement
session = db.session

def getTimeQhawaxHistory(name):
    """
    Get time qHAWAX History

    :type installation_id: integer
    :param installation_id: Installation ID

    """
    fields = (QhawaxInstallationHistory.last_time_physically_turn_on_zone,\
              QhawaxInstallationHistory.last_registration_time_zone)
    installation_id = same_helper.getInstallationIdBaseName(name)
    return None if (installation_id is None) else session.query(*fields).\
                                                        filter_by(id= installation_id).first()

def queryQhawaxModeCustomer():
    """
    Get qHAWAX list in mode Customer and state ON

    No parameters required

    """
    qhawax_column = (Qhawax.id, Qhawax.name, Qhawax.main_inca, Qhawax.qhawax_type,\
                     QhawaxInstallationHistory.comercial_name, EcaNoise.area_name)

    return session.query(*qhawax_column).\
                          join(Qhawax, QhawaxInstallationHistory.qhawax_id == Qhawax.id). \
                          join(EcaNoise, QhawaxInstallationHistory.eca_noise_id == EcaNoise.id). \
                          group_by(Qhawax.id, QhawaxInstallationHistory.id,EcaNoise.id). \
                          filter(Qhawax.mode =="Cliente", \
                                 Qhawax.state =="ON", \
                                 QhawaxInstallationHistory.end_date_zone == None).order_by(Qhawax.id).all()

def queryGetAreas():
    """
    Helper Eca Noise function to list all zones 

    No parameters required

    """
    fields = (EcaNoise.id, EcaNoise.area_name)
    areas = session.query(*fields).all()
    return None if (areas is []) else session.query(*fields).order_by(EcaNoise.id.desc()).all()

def queryGetEcaNoise(eca_noise_id):
    """
    Helper Eca Noise function to get zone description

    :type eca_noise_id: integer
    :param eca_noise_id: Eca Noise ID

    """
    fields = (EcaNoise.id, EcaNoise.area_name, EcaNoise.max_daytime_limit, \
              EcaNoise.max_night_limit)
    if(same_helper.areaExistBasedOnID(eca_noise_id)):
        return session.query(*fields).filter_by(id= eca_noise_id).first()
    return None

def getOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.WE, GasSensor.AE, \
                  GasSensor.sensitivity, GasSensor.sensitivity_2)

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        offsets_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        offset_json = {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}
        return util_helper.gasSensorJson(offset_json,offsets_sensors)
    return None


def getControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get controlled offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.C2, GasSensor.C1, GasSensor.C0)

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        controlled_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        controlled_offset_json = {'C0': 0.0, 'C1': 0.0, 'C2': 0.0}
        return util_helper.gasSensorJson(controlled_offset_json,controlled_sensors)
    return None

def getNonControlledOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get non controlled offsets from qHAWAX name

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    attributes = (GasSensor.type, GasSensor.NC1, GasSensor.NC0)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        non_controlled_sensors = session.query(*attributes).filter_by(qhawax_id=qhawax_id).all()
        non_controlled_offsets = {'NC1': 0.0, 'NC0': 0.0}
        return util_helper.gasSensorJson(non_controlled_offsets,non_controlled_sensors)
    return None


def queryIncaQhawax(name):
    """
    Helper qHAWAX function to get main inca value

    :type name: string
    :param name: qHAWAX name

    """
    qhawax_id = same_helper.getQhawaxID(name)
    if(qhawax_id is not None):
        qhawax_inca = int(same_helper.getMainIncaQhawaxTable(qhawax_id))
        return util_helper.getColorBaseOnIncaValue(qhawax_inca)
    return None


def getInstallationDate(qhawax_id):
    """
    Helper qHAWAX function to get Installation Date

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        return session.query(QhawaxInstallationHistory.installation_date_zone).\
                       filter(QhawaxInstallationHistory.id == installation_id).first()[0]
    return None

def getFirstTimestampValidProcessed(qhawax_id):
    """
    Helper qHAWAX Installation function to get first timestamp of Valid Processed 

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        first_timestamp =session.query(ValidProcessedMeasurement.timestamp_zone). \
                                 filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                 order_by(ValidProcessedMeasurement.timestamp_zone.asc()).first()
        return None if (first_timestamp==None) else first_timestamp[0]
    return None


def queryGetLastQhawax():
    """
    Helper qHAWAX function to get last qHAWAX ID

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    qhawax_list = session.query(Qhawax.id).all()
    return None if (qhawax_list== []) else session.query(Qhawax.id).\
                                                   order_by(Qhawax.id.desc()).all()[0]

def queryGetLastGasSensor():
    """
    Helper Gas Sensor function to get last Gas Sensor ID

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    gas_sensor_list = session.query(GasSensor.id).all()
    return None if(gas_sensor_list==[]) else session.query(GasSensor.id).\
                                                     order_by(GasSensor.id.desc()).all()[0]

def isItFieldQhawax(qhawax_name):
    """
    Check qhawax in field

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    return True if (same_helper.getInstallationIdBaseName(qhawax_name)is not None) else False

def getLatestTimeInProcessedMeasurement(qhawax_name):
    """
    Helper qHAWAX function to get latest timestamp in UTC 00 from Processed Measurement
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name
    
    """

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
        processed_measurement_timestamp=""
        qhawax_time = session.query(ProcessedMeasurement.timestamp_zone).\
                              filter_by(qhawax_id=qhawax_id).first()
        if(qhawax_time!=None):
            processed_measurement_timestamp = session.query(ProcessedMeasurement.timestamp_zone).\
                                                      filter_by(qhawax_id=qhawax_id).\
                                                      order_by(ProcessedMeasurement.id.desc()).\
                                                      first().timestamp_zone
        return processed_measurement_timestamp
    return None

def getLatestTimeInValidProcessed(qhawax_name):
    """
    Helper qHAWAX function to get latest timestamp in UTC 00 from Valid Processed Measurement
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name
    
    """
    installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        valid_processed_timestamp = ""
        qhawax_time = session.query(ValidProcessedMeasurement.timestamp_zone).\
                              filter_by(qhawax_installation_id=installation_id).first()
        if(qhawax_time!=None):
            return session.query(ValidProcessedMeasurement.timestamp_zone).\
                                                filter_by(qhawax_installation_id=installation_id). \
                                                order_by(ValidProcessedMeasurement.timestamp_zone.desc()).\
                                                first().timestamp_zone
    return None


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

def getQhawaxMode(qhawax_name):
    """
    Get qHAWAX mode based on name

    """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.mode).filter_by(name=qhawax_name).one()[0]
    return None

def getQhawaxStatus(qhawax_name):
    """
    Get qHAWAX status based on name

    """
    if(same_helper.qhawaxExistBasedOnName(qhawax_name)):
        return session.query(Qhawax.state).filter_by(name=qhawax_name).one()[0]
    return None
