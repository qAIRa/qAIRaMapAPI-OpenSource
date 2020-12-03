import project.main.business.post_business_helper as post_business_helper
from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, \
                                    ValidProcessedMeasurement, Qhawax, QhawaxInstallationHistory, EcaNoise, \
                                    AirDailyMeasurement
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db, socketio

session = db.session

def storeAirQualityDataInDB(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Air Quality variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!=None):
        data['uv'] = data['UV']
        data['spl'] = data['SPL']
        data.pop('SPL', None)
        data.pop('UV', None)
        air_quality_measurement = AirQualityMeasurement(**data, qhawax_id=qhawax_id)
        session.add(air_quality_measurement)
        session.commit()

def storeGasIncaInDB(data):
    """ Helper function to record GAS INCA measurement"""
    if(isinstance(data, dict) is not True):
        raise TypeError("Gas Inca variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_processed = GasInca(**data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()
                                  
def storeProcessedDataInDB(data):
    """ Helper Processed Measurement function to store Processed Data """
    if(isinstance(data, dict) is not True):
        raise TypeError("Processed variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()

def storeValidProcessedDataInDB(data, qhawax_id, product_id):
    """ Helper Processed Measurement function to insert Valid Processed Data """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id!=None):
      valid_data = {'timestamp': data['timestamp'],'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'], 
                    'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],
                    'SO2_ug_m3': data['SO2_ug_m3'],'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],
                    'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],'PM25': data['PM25'],
                    'lat':data['lat'],'lon':data['lon'],'PM1': data['PM1'],'PM10': data['PM10'],
                    'UV': data['UV'],'UVA': data['UVA'],'UVB': data['UVB'],'SPL': data['spl'],
                    'humidity': data['humidity'],'pressure': data['pressure'],
                    'temperature': data['temperature'],'timestamp_zone': data['timestamp_zone'],
                    'I_temperature':data['I_temperature'],'VOC':data['VOC'], 'CO2':data['CO2']}
      valid_processed_measurement = ValidProcessedMeasurement(**valid_data, qhawax_installation_id=installation_id)
      session.add(valid_processed_measurement)
      session.commit()
      data = util_helper.setNoneStringElements(data)
      socketio.emit(data['ID'], data)

def validAndBeautyJsonValidProcessed(data_json,qhawax_id,product_id,inca_value):
    if(isinstance(data_json, dict) is not True):
        raise TypeError("Valid Processed variable "+str(data_json)+" should be Json")

    storeValidProcessedDataInDB(data_json, qhawax_id)
    if(inca_value==0.0):
      post_business_helper.updateMainIncaInDB(1,product_id)

def storeAirDailyQualityDataInDB(data):
    """  Helper Daily Air Measurement function to store air daily measurement """
    if(isinstance(data, dict) is not True):
        raise TypeError("Valid Processed variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id is not None):
      data['spl'] = data['SPL']
      data.pop('SPL', None)
      data.pop('lat', None)
      data.pop('lon', None)
      data.pop('I_temperature', None)
      air_daily_quality_measurement = AirDailyMeasurement(**data, qhawax_id=qhawax_id)
      session.add(air_daily_quality_measurement)
      session.commit()
