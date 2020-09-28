import datetime
import dateutil
import dateutil.parser
import time
from project import app, db
from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, \
                                    ValidProcessedMeasurement, Qhawax, QhawaxInstallationHistory, EcaNoise, \
                                    AirDailyMeasurement
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
import project.main.business.post_business_helper as post_business_helper

session = db.session

def getQhawaxMode(qhawax_id):
    """
    Helper Processed Measurement function to get qHAWAX mode

    """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        return session.query(Qhawax.mode).filter_by(id=qhawax_id).one()[0]
    return None

def getComercialName(qhawax_id):
    """
    Helper Processed Measurement function to get qHAWAX comercial name

    """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        return session.query(QhawaxInstallationHistory.comercial_name).\
                       filter_by(id=installation_id).one()[0]
    return None

def queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp,date_format):
    sensors = (AirQualityMeasurement.CO, AirQualityMeasurement.H2S, AirQualityMeasurement.NO2,
                    AirQualityMeasurement.O3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                    AirQualityMeasurement.SO2, AirQualityMeasurement.lat, AirQualityMeasurement.lon, 
                    AirQualityMeasurement.alt, AirQualityMeasurement.timestamp_zone)

    initial_timestamp_utc = datetime.datetime.strptime(initial_timestamp, date_format)
    final_timestamp_utc = datetime.datetime.strptime(final_timestamp, date_format)

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!=None):
        air_quality_measurements= session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                          filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp). \
                                          filter(AirQualityMeasurement.timestamp_zone <= final_timestamp). \
                                          order_by(AirQualityMeasurement.timestamp_zone).all()
        if(air_quality_measurements is not []):
            return [measurement._asdict() for measurement in air_quality_measurements]
        return []
    return None


def getTimeQhawaxHistory(installation_id):
    fields = (QhawaxInstallationHistory.last_time_physically_turn_on_zone, 
              QhawaxInstallationHistory.last_registration_time_zone)

    if(isinstance(installation_id, int) is not True):  
        raise TypeError("Installation ID "+str(installation_id)+" should be integer")

    values= session.query(*fields).filter(QhawaxInstallationHistory.id == installation_id).first()
    if (values!=None):
        print({'last_time_on': values[0], 'last_time_registration': values[1]} )
        return {'last_time_on': values[0], 'last_time_registration': values[1]} 
    return None

def queryDBGasAverageMeasurement(qhawax_name, gas_name):
    """
    Helper function to get gas average measurement based on qHAWAX name and sensor name
    """
    sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']

    if(isinstance(gas_name, str) is not True):  
        raise TypeError("Sensor name "+str(gas_name)+" should be string")

    if(gas_name not in sensor_array):
        raise ValueError("Sensor name "+str(gas_name)+" should be CO, H2S, NO2, O3, PM25, PM10 or SO2")

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!= None):
        installation_id = same_helper.getInstallationId(qhawax_id)
        if(installation_id!=None):
            values_list = getTimeQhawaxHistory(installation_id)
            
            initial_timestamp = datetime.datetime.now()
            last_timestamp = datetime.datetime.now() - datetime.timedelta(hours=24)
            
            column_array = [AirQualityMeasurement.CO.label('sensor'), AirQualityMeasurement.H2S.label('sensor'), 
                            AirQualityMeasurement.NO2.label('sensor'), AirQualityMeasurement.O3.label('sensor'),
                            AirQualityMeasurement.PM25.label('sensor'), AirQualityMeasurement.PM10.label('sensor'),
                            AirQualityMeasurement.SO2.label('sensor')]

            for i in range(len(sensor_array)):
                if(gas_name==sensor_array[i]):
                    sensors = (AirQualityMeasurement.timestamp_zone, column_array[i])

            last_time_turn_on = values_list['last_time_on']
            last_registration_time = values_list['last_time_registration']

            return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                       filter(AirQualityMeasurement.timestamp_zone >= last_timestamp). \
                                       filter(AirQualityMeasurement.timestamp_zone <= initial_timestamp). \
                                       order_by(AirQualityMeasurement.timestamp_zone.asc()).all()
    return None


def queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp,date_format):
    """
    Helper function to get Air Quality measurement

    """
    sensors = (AirQualityMeasurement.CO_ug_m3, AirQualityMeasurement.H2S_ug_m3, AirQualityMeasurement.NO2_ug_m3,
                AirQualityMeasurement.O3_ug_m3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                AirQualityMeasurement.SO2_ug_m3, AirQualityMeasurement.uv,AirQualityMeasurement.uva, 
                AirQualityMeasurement.uvb, AirQualityMeasurement.spl,AirQualityMeasurement.humidity, 
                AirQualityMeasurement.pressure, AirQualityMeasurement.temperature, AirQualityMeasurement.lat, 
                AirQualityMeasurement.lon, AirQualityMeasurement.timestamp_zone)

    initial_timestamp = datetime.datetime.strptime(initial_timestamp, '%d-%m-%Y %H:%M:%S')
    final_timestamp = datetime.datetime.strptime(final_timestamp, '%d-%m-%Y %H:%M:%S')
    
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        average_valid_processed= session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                        filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp). \
                                        filter(AirQualityMeasurement.timestamp_zone <= final_timestamp). \
                                        order_by(AirQualityMeasurement.timestamp).all()
        if(average_valid_processed is not []):
            return [measurement._asdict() for measurement in average_valid_processed]
        return []
    return None

def queryDBGasInca(initial_timestamp, final_timestamp,date_format):
    """
    Helper function to get GAS INCA measurement

    """
    sensors = (GasInca.CO, GasInca.H2S, GasInca.SO2, GasInca.NO2,GasInca.O3, 
               GasInca.PM25, GasInca.PM10, GasInca.SO2,GasInca.timestamp_zone, 
               GasInca.qhawax_id, GasInca.main_inca, Qhawax.name.label('qhawax_name'))
    
    if(isinstance(initial_timestamp, str) is not True):  
        raise TypeError("Initial timestamp"+str(initial_timestamp)+" should be string")

    if(isinstance(final_timestamp, str) is not True):  
        raise TypeError("Last timestamp"+str(final_timestamp)+" should be string")

    initial_timestamp = datetime.datetime.strptime(initial_timestamp, date_format)
    final_timestamp = datetime.datetime.strptime(final_timestamp, date_format)

    gas_inca = session.query(*sensors).\
                       join(Qhawax, GasInca.qhawax_id == Qhawax.id). \
                       group_by(Qhawax.id, GasInca.id). \
                       filter(GasInca.timestamp_zone >= initial_timestamp). \
                       filter(GasInca.timestamp_zone <= final_timestamp).all()
    if(gas_inca is not []):
        return [measurement._asdict() for measurement in gas_inca]
    return []
                                  
def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp,date_format):

    if(isinstance(initial_timestamp, str) is not True):  
        raise TypeError("Initial timestamp"+str(initial_timestamp)+" should be string")

    if(isinstance(final_timestamp, str) is not True):  
        raise TypeError("Last timestamp"+str(final_timestamp)+" should be string")

    initial_timestamp = datetime.datetime.strptime(initial_timestamp, date_format)
    final_timestamp = datetime.datetime.strptime(final_timestamp, date_format)

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):

        sensors = (ProcessedMeasurement.CO, ProcessedMeasurement.CO2, ProcessedMeasurement.H2S, ProcessedMeasurement.NO,
                    ProcessedMeasurement.NO2, ProcessedMeasurement.O3, ProcessedMeasurement.PM1, ProcessedMeasurement.PM25,
                    ProcessedMeasurement.PM10, ProcessedMeasurement.SO2, ProcessedMeasurement.VOC, ProcessedMeasurement.UV,
                    ProcessedMeasurement.UVA, ProcessedMeasurement.UVB, ProcessedMeasurement.spl, ProcessedMeasurement.humidity,
                    ProcessedMeasurement.pressure, ProcessedMeasurement.temperature, ProcessedMeasurement.lat,
                    ProcessedMeasurement.lon, ProcessedMeasurement.alt, ProcessedMeasurement.timestamp_zone)

        processed_measurements = session.query(*sensors).filter(ProcessedMeasurement.qhawax_id == qhawax_id). \
                                         filter(ProcessedMeasurement.timestamp_zone > initial_timestamp). \
                                         filter(ProcessedMeasurement.timestamp_zone < final_timestamp). \
                                         order_by(ProcessedMeasurement.timestamp).all()
        if(processed_measurements is not []):                                 
            return [measurement._asdict() for measurement in processed_measurements]
        return []
    return None

def getNoiseData(qhawax_name):
    """
    Helper Processed Measurement function to get Noise Area Description

    """
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        eca_noise_id = session.query(QhawaxInstallationHistory.eca_noise_id).\
                               filter_by(id=installation_id).first()
        return session.query(EcaNoise.area_name).filter_by(id=eca_noise_id).first()[0]
    return None

def getHoursDifference(qhawax_id):
    """
    Helper Processed Measurement function to get 
    minutes difference between last_registration_time and last_time_physically_turn_on

    """
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
        values = session.query(QhawaxInstallationHistory.last_time_physically_turn_on_zone, \
                               QhawaxInstallationHistory.last_registration_time_zone).\
                         filter(QhawaxInstallationHistory.qhawax_id == qhawax_id).first()
        if (values[0]!=None and values[1]!=None):
            minutes_difference = int((values[0] - values[1]).total_seconds() / 60)
            return minutes_difference, values[0]
    return None, None

def queryDBValidProcessedByQhawaxScript(qhawax_id, initial_timestamp, final_timestamp,date_format):
    """
    Helper Valid Processed Measurement function to get valid data to daily table
    """
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,
               ValidProcessedMeasurement.H2S_ug_m3,ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3, 
               ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, ValidProcessedMeasurement.PM25,
               ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
               ValidProcessedMeasurement.UV, ValidProcessedMeasurement.UVA,ValidProcessedMeasurement.UVB,
               ValidProcessedMeasurement.SPL, ValidProcessedMeasurement.humidity,ValidProcessedMeasurement.pressure, 
               ValidProcessedMeasurement.temperature, ValidProcessedMeasurement.lat,ValidProcessedMeasurement.lon, 
               ValidProcessedMeasurement.timestamp_zone)

    if(isinstance(initial_timestamp, str) is not True):  
        raise TypeError("Initial timestamp"+str(initial_timestamp)+" should be string")

    if(isinstance(final_timestamp, str) is not True):  
        raise TypeError("Last timestamp"+str(final_timestamp)+" should be string")

    initial_timestamp = datetime.datetime.strptime(initial_timestamp, date_format)
    final_timestamp = datetime.datetime.strptime(final_timestamp, date_format)
    installation_id = same_helper.getInstallationId(qhawax_id)

    if(installation_id is not None):
        valid_processed_measurements = session.query(*sensors).\
                                       filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                       filter(ValidProcessedMeasurement.timestamp_zone >= initial_timestamp). \
                                       filter(ValidProcessedMeasurement.timestamp_zone <= final_timestamp). \
                                       order_by(ValidProcessedMeasurement.timestamp_zone).all()
        if (valid_processed_measurements is not []):
            return [measurement._asdict() for measurement in valid_processed_measurements]
        return []
    return None

def getLatestTimestampValidProcessed(qhawax_name):
    """
    Helper Valid Processed Measurement function to get latest timestamp by qHAWAX name
    """
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if(installation_id is not None):
        time_valid_data = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                  filter_by(qhawax_installation_id=installation_id).first()
        valid_processed_measurement_timestamp = []
        if(time_valid_data!=None):
            valid_processed_measurement_timestamp = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                                            filter_by(qhawax_installation_id=installation_id). \
                                                            order_by(ValidProcessedMeasurement.id.desc()).\
                                                            first().timestamp_zone
        return valid_processed_measurement_timestamp
    return None

def queryDBDailyValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp,date_format):
    """
    Helper Valid Processed Measurement function to valid measurement filter by time
    """
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,
               ValidProcessedMeasurement.H2S_ug_m3,ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3,
               ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, ValidProcessedMeasurement.PM25,
               ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
               ValidProcessedMeasurement.humidity,ValidProcessedMeasurement.pressure, ValidProcessedMeasurement.temperature, 
               ValidProcessedMeasurement.timestamp_zone)

    if(isinstance(initial_timestamp, str) is not True):  
        raise TypeError("Initial timestamp"+str(initial_timestamp)+" should be string")

    if(isinstance(final_timestamp, str) is not True):  
        raise TypeError("Last timestamp"+str(final_timestamp)+" should be string")

    initial_timestamp = datetime.datetime.strptime(initial_timestamp,date_format)
    final_timestamp = datetime.datetime.strptime(final_timestamp, date_format)

    if(same_helper.qhawaxInstallationExistBasedOnID(installation_id)):
        valid_processed = session.query(*sensors). \
                                  filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                  filter(ValidProcessedMeasurement.timestamp_zone > initial_timestamp). \
                                  filter(ValidProcessedMeasurement.timestamp_zone < final_timestamp). \
                                  order_by(ValidProcessedMeasurement.timestamp_zone).all()
        if(valid_processed is not []):
            return [daily_valid_measurement._asdict() for daily_valid_measurement in valid_processed]
        return []
    return None


def queryDBAirDailyQuality(qhawax_id, init_week, init_year,end_week, end_year):
    """
    Air Daily Measurement function helper to get daily average measurement based on week number and year 

    """

    sensors = (AirDailyMeasurement.CO, AirDailyMeasurement.H2S, AirDailyMeasurement.NO2,
                AirDailyMeasurement.O3, AirDailyMeasurement.PM25, AirDailyMeasurement.PM10, 
                AirDailyMeasurement.SO2, AirDailyMeasurement.timestamp_zone)

    if(type(init_week) not in [int]):
        raise TypeError("Initial week number should be int")

    if(type(init_year) not in [int]):
        raise TypeError("Initial year number should be int")

    if(type(end_week) not in [int]):
        raise TypeError("Last week number should be int")

    if(type(end_year) not in [int]):
        raise TypeError("Last year number should be int")

    if(end_week<init_week):
        raise ValueError("End week must be higher than init week")

    if(end_year<init_year):
        raise ValueError("End year must be higher or equal than init year")


    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):

        init_firstdate, init_lastdate =  util_helper.getDateRangeFromWeek(init_year,init_week)
        end_firstdate, end_lastdate =  util_helper.getDateRangeFromWeek(end_year,end_week)

        air_daily_measurements = session.query(*sensors).filter(AirDailyMeasurement.qhawax_id == qhawax_id). \
                                         filter(AirDailyMeasurement.timestamp_zone >= init_firstdate). \
                                         filter(AirDailyMeasurement.timestamp_zone <= end_lastdate). \
                                         order_by(AirDailyMeasurement.timestamp_zone).all()
        if(air_daily_measurements is not []):
            return [measurement._asdict() for measurement in air_daily_measurements]
        return []
    return None

