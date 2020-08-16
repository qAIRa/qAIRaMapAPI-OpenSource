import time
from project import app, db
import string

import project.database.utils as utils
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

from project.database.models import GasSensor, Qhawax, EcaNoise, QhawaxInstallationHistory, \
                                    Company, AirQualityMeasurement, ProcessedMeasurement, \
                                    ValidProcessedMeasurement

session = db.session


def getTimeQhawaxHistory(installation_id):
    values= session.query(QhawaxInstallationHistory.last_time_physically_turn_on_zone,\
                          QhawaxInstallationHistory.last_registration_time_zone).\
                    filter(QhawaxInstallationHistory.id == installation_id).first()
    if (values!=None):
        return values
    else:
        return None

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
    sensors = (Company.id, Company.name, Company.email_group, Company.ruc, 
               Company.address, Company.phone, Company.contact_person)
    companies = session.query(*sensors).all()
    if(companies == []):
        return None
    return session.query(*sensors).order_by(Company.id.desc()).all()

def queryGetAreas():
    """
    Helper Eca Noise function to list all zones 

    No parameters required

    """
    sensors = (EcaNoise.id, EcaNoise.area_name)
    return session.query(*sensors).order_by(EcaNoise.id.desc()).all()

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


def getOffsetsFromProductID(qhawax_name):
    """
    Helper Gas Sensor function to get offsets from qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    if(isinstance(qhawax_name, str)):
        qhawax_id = same_helper.getQhawaxID(qhawax_name)

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
        qhawax_id = same_helper.getQhawaxID(qhawax_name)

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
        qhawax_id = same_helper.getQhawaxID(qhawax_name)

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

def getInstallationDateByQhawaxID(qhawax_id):
    installation_date = session.query(QhawaxInstallationHistory.installation_date_zone).\
                                filter_by(qhawax_id=qhawax_id). \
                                filter(QhawaxInstallationHistory.end_date_zone == None). \
                                order_by(QhawaxInstallationHistory.installation_date_zone.desc()).first()
    if (installation_date==None):
        return installation_date
    return installation_date[0]

def getFirstTimestampValidProcessed(qhawax_installation_id):

    first_timestamp =session.query(ValidProcessedMeasurement.timestamp_zone). \
                             filter(ValidProcessedMeasurement.qhawax_installation_id == int(qhawax_installation_id)). \
                             order_by(ValidProcessedMeasurement.timestamp_zone.asc()).first()                  
    if (first_timestamp==None):
        return first_timestamp
    return first_timestamp[0]

def getMainIncaQhawax(name):
    installation_id=same_helper.getInstallationIdBaseName(name)
    qhawax_inca = session.query(QhawaxInstallationHistory.main_inca).filter_by(id=installation_id).one()[0]
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
        qhawax_list = session.query(Qhawax.id).filter_by(name=qhawax_name).all()
        if(qhawax_list == []):
            raise TypeError("The qHAWAX name could not be found")
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).one().id
        qhawax_time = session.query(ProcessedMeasurement.timestamp_zone).filter_by(qhawax_id=qhawax_id).first()
        processed_measurement_timestamp=""
        if(qhawax_time!=None):
            processed_measurement_timestamp = session.query(ProcessedMeasurement.timestamp_zone).filter_by(qhawax_id=qhawax_id) \
                .order_by(ProcessedMeasurement.id.desc()).first().timestamp_zone
        return processed_measurement_timestamp
    else:
        raise TypeError("The qhawax name should be string")


def getQhawaxLatestTimestampValidProcessedMeasurement(qhawax_name):
    if(isinstance(qhawax_name, str)):
        installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
        valid_processed_measurement_timestamp=""
        if(installation_id != None):
            qhawax_time = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                  filter_by(qhawax_installation_id=installation_id).first()
            if(qhawax_time!=None):
                valid_processed_measurement_timestamp = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                                                filter_by(qhawax_installation_id=installation_id) \
                                                                .order_by(ValidProcessedMeasurement.timestamp_zone.desc()).first().timestamp_zone
        
        return valid_processed_measurement_timestamp
    else:
        raise TypeError("The qhawax name should be string")

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

