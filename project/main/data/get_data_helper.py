from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, \
                                    ValidProcessedMeasurement, Qhawax, QhawaxInstallationHistory, EcaNoise, \
                                    AirDailyMeasurement
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
import project.main.business.post_business_helper as post_business_helper
from project import app, db
import datetime
import math

session = db.session

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
        return [measurement._asdict() for measurement in air_quality_measurements]
    return None

def queryDBGasAverageMeasurement(qhawax_name, gas_name):
    """ Helper function to get gas average measurement based on qHAWAX name and sensor name"""
    sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']

    if(isinstance(gas_name, str) is not True):  
        raise TypeError("Sensor name "+str(gas_name)+" should be string")

    if(gas_name not in sensor_array):
        raise ValueError("Sensor name "+str(gas_name)+" should be CO, H2S, NO2, O3, PM25, PM10 or SO2")

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!= None):
        installation_id = same_helper.getInstallationId(qhawax_id)
        if(installation_id!=None):
            values_list = same_helper.getTimeQhawaxHistory(installation_id)
            
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

def queryDBGasInca(initial_timestamp, final_timestamp,date_format):
    """ Helper function to get GAS INCA measurement"""
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
    return [measurement._asdict() for measurement in gas_inca]
                                  
def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp,date_format):

    if(isinstance(initial_timestamp, str) is not True):  
        raise TypeError("Initial timestamp"+str(initial_timestamp)+" should be string")

    if(isinstance(final_timestamp, str) is not True):  
        raise TypeError("Last timestamp"+str(final_timestamp)+" should be string")

    initial_timestamp = datetime.datetime.strptime(initial_timestamp, date_format)
    final_timestamp = datetime.datetime.strptime(final_timestamp, date_format)

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):

        sensors = (ProcessedMeasurement.CO, ProcessedMeasurement.CO2, ProcessedMeasurement.H2S,ProcessedMeasurement.NO,
                   ProcessedMeasurement.NO2, ProcessedMeasurement.O3, ProcessedMeasurement.PM1,ProcessedMeasurement.PM25,
                   ProcessedMeasurement.PM10,ProcessedMeasurement.SO2, ProcessedMeasurement.VOC, ProcessedMeasurement.UV,
                   ProcessedMeasurement.UVA, ProcessedMeasurement.UVB, ProcessedMeasurement.spl, ProcessedMeasurement.humidity,
                   ProcessedMeasurement.pressure, ProcessedMeasurement.temperature, ProcessedMeasurement.lat,
                   ProcessedMeasurement.lon, ProcessedMeasurement.alt, ProcessedMeasurement.timestamp_zone,
                   ProcessedMeasurement.CO_ug_m3, ProcessedMeasurement.H2S_ug_m3, ProcessedMeasurement.NO2_ug_m3,
                   ProcessedMeasurement.O3_ug_m3, ProcessedMeasurement.SO2_ug_m3, ProcessedMeasurement.I_temperature)

        processed_measurements = session.query(*sensors).filter(ProcessedMeasurement.qhawax_id == qhawax_id). \
                                         filter(ProcessedMeasurement.timestamp_zone >= initial_timestamp). \
                                         filter(ProcessedMeasurement.timestamp_zone <= final_timestamp). \
                                         order_by(ProcessedMeasurement.timestamp_zone).all()
        all_measurement = []
        for measurement in processed_measurements:
          measurement = measurement._asdict()
          for key, value in measurement.items():
            if((type(value) is float) and math.isnan(value)): measurement[key] = None
          all_measurement.append(measurement)
        return all_measurement
    return None

def queryDBValidProcessedByQhawaxScript(qhawax_id, initial_timestamp, final_timestamp,date_format):
    """Helper Valid Processed Measurement function to get valid data to daily table"""
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
        return [measurement._asdict() for measurement in valid_processed_measurements]
    return None

def getLatestTimestampValidProcessed(qhawax_name):
    """ Helper Valid Processed Measurement function to get latest timestamp by qHAWAX name"""
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
    """ Helper Valid Processed Measurement function to valid measurement filter by time """
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
        return [daily_valid_measurement._asdict() for daily_valid_measurement in valid_processed]
    return None

def queryDBAirDailyQuality(qhawax_id, init_week, init_year,end_week, end_year):
    """ Air Daily Measurement function helper to get daily average measurement based on week number and year """

    sensors = (AirDailyMeasurement.CO, AirDailyMeasurement.CO_ug_m3,AirDailyMeasurement.H2S, 
               AirDailyMeasurement.H2S_ug_m3, AirDailyMeasurement.NO2, AirDailyMeasurement.NO2_ug_m3,
               AirDailyMeasurement.O3, AirDailyMeasurement.O3_ug_m3, AirDailyMeasurement.PM25, 
               AirDailyMeasurement.PM10, AirDailyMeasurement.SO2, AirDailyMeasurement.SO2_ug_m3,
               AirDailyMeasurement.timestamp_zone,AirDailyMeasurement.UV, AirDailyMeasurement.spl,
               AirDailyMeasurement.humidity, AirDailyMeasurement.pressure, AirDailyMeasurement.temperature)

    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):

        init_firstdate, init_lastdate =  util_helper.getDateRangeFromWeek(init_year,init_week)
        end_firstdate, end_lastdate =  util_helper.getDateRangeFromWeek(end_year,end_week)

        if(str(init_firstdate)>str(end_lastdate)):
            raise ValueError("init_week and init_year must be lower than end_week and end_year")

        air_daily_measurements = session.query(*sensors).filter(AirDailyMeasurement.qhawax_id == qhawax_id). \
                                         filter(AirDailyMeasurement.timestamp_zone >= init_firstdate). \
                                         filter(AirDailyMeasurement.timestamp_zone <= end_lastdate). \
                                         order_by(AirDailyMeasurement.timestamp_zone).all()
        return [measurement._asdict() for measurement in air_daily_measurements]
    return None


