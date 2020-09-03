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

def storeAirQualityDataInDB(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("Air Quality variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    data['uv'] = data['UV']
    data['spl'] = data['SPL']
    data.pop('SPL', None)
    data.pop('UV', None)
    air_quality_measurement = AirQualityMeasurement(**data, qhawax_id=qhawax_id)
    session.add(air_quality_measurement)
    session.commit()


def storeGasIncaInDB(data):
    """
    Helper function to record GAS INCA measurement

    :type data: json
    :param data: gas inca measurement

    """
    if(isinstance(data, dict) is not True):
        raise TypeError("Gas Inca variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_processed = GasInca(**data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()
                                  

def storeProcessedDataInDB(data):
    """
    Helper Processed Measurement function to store Processed Data

    :type data: json
    :param data: Processed Measurement detail

    """
    if(isinstance(data, dict) is not True):
        raise TypeError("Processed variable "+str(data)+" should be Json")

    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()


def storeValidProcessedDataInDB(data, qhawax_id):
    """
    Helper Processed Measurement function to insert Valid Processed Data
    """

    if(isinstance(data, dict) is not True):
        raise TypeError("Valid Processed variable "+str(data)+" should be Json")
    
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id!=None):
        valid_data = {'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'], 
                      'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],
                      'SO2_ug_m3': data['SO2_ug_m3'],'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],
                      'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],'PM25': data['PM25'],
                      'lat':data['lat'],'lon':data['lon'],'PM1': data['PM1'],'PM10': data['PM10'],
                      'UV': data['UV'],'UVA': data['UVA'],'UVB': data['UVB'],'SPL': data['spl'],
                      'humidity': data['humidity'],'pressure': data['pressure'],
                      'temperature': data['temperature'],'timestamp_zone': data['timestamp_zone']}
        valid_processed_measurement = ValidProcessedMeasurement(**valid_data, qhawax_installation_id=installation_id)
        session.add(valid_processed_measurement)
        session.commit()
                     

def storeAirDailyQualityDataInDB(data):
    """
    Helper Daily Air Measurement function to store air daily measurement

    :type data: json
    :param data: json of average of daily measurement

    """
    if(isinstance(data, dict) is not True):
        raise TypeError("Valid Processed variable "+str(data)+" should be Json")
        
    qhawax_name = data.pop('ID', None)
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    
    air_daily_quality_data = {'CO': data['CO'], 'CO_ug_m3': data['CO_ug_m3'],'H2S': data['H2S'], 
                              'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'],
                              'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],
                              'O3_ug_m3': data['O3_ug_m3'], 'PM25': data['PM25'], 'PM10': data['PM10'], 
                              'timestamp_zone': data['timestamp_zone'], 'humidity':data['humidity'],
                              'pressure':data['pressure'],'temperature':data['temperature']}

    air_daily_quality_measurement = AirDailyMeasurement(**air_daily_quality_data, qhawax_id=qhawax_id)
    session.add(air_daily_quality_measurement)
    session.commit()
