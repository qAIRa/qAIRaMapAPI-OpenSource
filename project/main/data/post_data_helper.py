from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, ValidProcessedMeasurement
import project.main.business.post_business_helper as post_business_helper
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
import project.main.exceptions as exceptions
from project import app, db, socketio
from datetime import timedelta
import dateutil.parser
import dateutil.tz
import datetime

session = db.session

def storeAirQualityDataInDB(data):
    data = exceptions.checkDictionaryVariable(data)
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!=None):
        air_quality_data = {'CO': data['CO'], 'CO_ug_m3': data['CO_ug_m3'],'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],
                          'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'],'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],
                          'O3_ug_m3': data['O3_ug_m3'], 'PM25': data['PM25'], 'PM10': data['PM10'], 'O3': data['O3'],
                          'lat': data['lat'],'lon': data['lon'], 'alt': data['alt'], 'uv':data['UV'],'spl':data['SPL'], 
                          'temperature':data['temperature'],'timestamp_zone': data['timestamp_zone'],
                          'I_temperature':data['I_temperature'],'humidity':data['humidity'],'pressure':data['pressure'],}
        air_quality_measurement = AirQualityMeasurement(**air_quality_data, qhawax_id=qhawax_id)
        session.add(air_quality_measurement)
        session.commit()

def storeGasIncaInDB(data):
    """ Helper function to record GAS INCA measurement"""
    data = exceptions.checkDictionaryVariable(data)
    gas_inca_data = {'CO': data['CO'],'H2S': data['H2S'],'SO2': data['SO2'],'NO2': data['NO2'],'timestamp_zone':data['timestamp_zone'],
                     'O3': data['O3'],'PM25': data['PM25'],'PM10': data['PM10'],'main_inca':data['main_inca']}
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_processed = GasInca(**gas_inca_data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()
                                  
def storeProcessedDataInDB(data):
    """ Helper Processed Measurement function to store Processed Data """
    data = exceptions.checkDictionaryVariable(data)
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()

def storeValidProcessedDataInDB(data, product_id):
    """ Helper Processed Measurement function to insert Valid Processed Data """
    installation_id = same_helper.getInstallationIdBaseName(product_id)
    if(installation_id!=None):
      valid_data = {'timestamp': data['timestamp'],'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'], 'H2S': data['H2S'],
                    'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'],'NO2': data['NO2'],
                    'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],'PM25': data['PM25'],
                    'lat':data['lat'],'lon':data['lon'],'PM1': data['PM1'],'PM10': data['PM10'], 'UV': data['UV'],
                    'UVA': data['UVA'],'UVB': data['UVB'],'SPL': data['spl'],'humidity': data['humidity'], 'CO2':data['CO2'],
                    'pressure': data['pressure'],'temperature': data['temperature'],'timestamp_zone': data['timestamp_zone'],
                    'I_temperature':data['I_temperature'],'VOC':data['VOC']}
      valid_processed_measurement = ValidProcessedMeasurement(**valid_data, qhawax_installation_id=installation_id)
      session.add(valid_processed_measurement)
      session.commit()
      data = util_helper.setNoneStringElements(data)
      socketio.emit(data['ID'], data)

def validAndBeautyJsonValidProcessed(data_json,product_id,inca_value):
    data_json = exceptions.checkDictionaryVariable(data_json)
    storeValidProcessedDataInDB(data_json,product_id)
    if(inca_value==0.0):
      post_business_helper.updateMainIncaQhawaxTable(1,product_id)
      post_business_helper.updateMainIncaQhawaxInstallationTable(1,product_id)

def validTimeOfValidProcessed(time_valid,time_type, last_time_turn_on,data_json,product_id,inca_value):
    aditional_time = datetime.timedelta(hours=time_valid) if (time_type=="hour") else datetime.timedelta(minutes=time_valid)
    if(last_time_turn_on + aditional_time < datetime.datetime.now(dateutil.tz.tzutc())):
      validAndBeautyJsonValidProcessed(data_json,product_id,inca_value)

