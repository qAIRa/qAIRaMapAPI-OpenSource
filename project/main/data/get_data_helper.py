from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca,ValidProcessedMeasurement, Qhawax
import project.main.business.post_business_helper as post_business_helper
import project.main.same_function_helper as same_helper
import project.main.exceptions as exceptions
from project import app, db
import datetime
import math

session = db.session

def queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp): #validar con sabri
    """ Helper function to get Air Quality measurement """
    sensors = (AirQualityMeasurement.CO_ug_m3, AirQualityMeasurement.H2S_ug_m3, AirQualityMeasurement.NO2_ug_m3, 
               AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, AirQualityMeasurement.SO2_ug_m3, 
               AirQualityMeasurement.uv.label('UV'), AirQualityMeasurement.spl.label('SPL') ,
               AirQualityMeasurement.humidity, AirQualityMeasurement.pressure, AirQualityMeasurement.O3_ug_m3, 
               AirQualityMeasurement.temperature, AirQualityMeasurement.lat,AirQualityMeasurement.lon, 
               AirQualityMeasurement.timestamp_zone)
    
    if(same_helper.qhawaxExistBasedOnID(qhawax_id)):
      valid_processed_measurements = session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                             filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp). \
                                             filter(AirQualityMeasurement.timestamp_zone <= final_timestamp). \
                                             order_by(AirQualityMeasurement.timestamp_zone).all()
      return [measurement._asdict() for measurement in valid_processed_measurements]
    return None

def queryDBGasAverageMeasurement(qhawax_name, gas_name):
    """ Helper function to get gas average measurement based on qHAWAX name and sensor name"""
    sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']
    gas_name = exceptions.checkStringVariable(gas_name)

    if(gas_name not in sensor_array):
        raise ValueError("Sensor name "+str(gas_name)+" should be CO, H2S, NO2, O3, PM25, PM10 or SO2")

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!= None):
        initial_timestamp = datetime.datetime.now()
        last_timestamp = datetime.datetime.now() - datetime.timedelta(hours=24)
        
        column_array = [AirQualityMeasurement.CO.label('sensor'), AirQualityMeasurement.H2S.label('sensor'), 
                        AirQualityMeasurement.NO2.label('sensor'), AirQualityMeasurement.O3.label('sensor'),
                        AirQualityMeasurement.PM25.label('sensor'), AirQualityMeasurement.PM10.label('sensor'),
                        AirQualityMeasurement.SO2.label('sensor')]

        for i in range(len(sensor_array)):
            if(gas_name==sensor_array[i]):
                sensors = (AirQualityMeasurement.timestamp_zone, column_array[i])

        return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                   filter(AirQualityMeasurement.timestamp_zone >= last_timestamp). \
                                   filter(AirQualityMeasurement.timestamp_zone <= initial_timestamp). \
                                   order_by(AirQualityMeasurement.timestamp_zone.asc()).all()
    return None

def queryDBGasInca(initial_timestamp, final_timestamp):
    """ Helper function to get GAS INCA measurement"""
    inca_columns = (GasInca.CO, GasInca.H2S, GasInca.SO2, GasInca.NO2,GasInca.O3, GasInca.PM25, GasInca.PM10, 
                    GasInca.SO2,GasInca.timestamp_zone, GasInca.qhawax_id, GasInca.main_inca, Qhawax.name.label('qhawax_name'))

    gas_inca = session.query(*inca_columns).\
                       join(Qhawax, GasInca.qhawax_id == Qhawax.id). \
                       group_by(Qhawax.id, GasInca.id). \
                       filter(GasInca.timestamp_zone >= initial_timestamp). \
                       filter(GasInca.timestamp_zone <= final_timestamp).all()
    return [measurement._asdict() for measurement in gas_inca]
                                  
def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp):
    """ Helper function to get Processed Measurement filter by qHAWAX between timestamp"""
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

def queryLastMainInca(qhawax_name):
    """Helper function to get last main inca based on qHAWAX ID """
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
      inca = session.query(GasInca.main_inca).filter(GasInca.qhawax_id == qhawax_id).order_by(GasInca.id).all()
      if(inca==[]):
        return None
      return session.query(GasInca.main_inca).filter(GasInca.qhawax_id == qhawax_id).order_by(GasInca.id.desc()).first()[0]
    return None

def getFirstTimestampValidProcessed(qhawax_id):
    """ Helper qHAWAX Installation function to get first timestamp of Valid Processed  """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id is not None):
        first_timestamp =session.query(ValidProcessedMeasurement.timestamp_zone). \
                                 filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                 order_by(ValidProcessedMeasurement.timestamp_zone.asc()).first()
        return None if (first_timestamp==None) else first_timestamp[0]
    return None
