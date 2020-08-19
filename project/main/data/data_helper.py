import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio
from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, \
                                    ValidProcessedMeasurement, Qhawax, QhawaxInstallationHistory, EcaNoise
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

session = db.session

def getMainIncaQhawaxTable(name):
    """
    Helper Processed Measurement function to get Main Inca from qHAWAX Table

    :type name: string
    :param name: qHAWAX name

    """
    if(isinstance(name, str)):
        qhawax_inca = session.query(Qhawax.main_inca).filter_by(name=name).all()
        if(qhawax_inca == []):
            raise TypeError("The qHAWAX name was not found")
        qhawax_inca = session.query(Qhawax.main_inca).filter_by(name=name).one()[0]
    else:
        raise TypeError("The qHAWAX name should be string")
    return qhawax_inca 


def getQhawaxMode(qhawax_id):
    """
    Helper Processed Measurement function to get qHAWAX mode

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    qhawax_mode = ""
    if(isinstance(qhawax_id, int)):
        qhawax_mode = session.query(Qhawax.mode).filter_by(id=qhawax_id).all()
        if(qhawax_mode == []):
            raise TypeError("The qHAWAX id could not be found")
        qhawax_mode = session.query(Qhawax.mode).filter_by(id=qhawax_id).one()[0]
    return qhawax_mode

def getComercialName(qhawax_id):
    """
    Helper Processed Measurement function to get qHAWAX comercial name

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(isinstance(qhawax_id, int)):
        comercial_name = session.query(QhawaxInstallationHistory.comercial_name).\
                                 filter_by(qhawax_id=qhawax_id, end_date_zone=None).all()
        if(comercial_name == []):
            raise TypeError("The qHAWAX comercial name could not be found")
        comercial_name = session.query(QhawaxInstallationHistory.comercial_name).\
                                 filter_by(qhawax_id=qhawax_id, end_date_zone=None).one()[0]
    return comercial_name

def queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if(qhawax_id!=None):
        sensors = (AirQualityMeasurement.CO, AirQualityMeasurement.H2S, AirQualityMeasurement.NO2,
                    AirQualityMeasurement.O3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                    AirQualityMeasurement.SO2, AirQualityMeasurement.lat, AirQualityMeasurement.lon, 
                    AirQualityMeasurement.alt, AirQualityMeasurement.timestamp_zone)
        
        return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                        filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp). \
                                        filter(AirQualityMeasurement.timestamp_zone <= final_timestamp). \
                                        order_by(AirQualityMeasurement.timestamp_zone).all()

def storeAirQualityDataInDB(data):
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    air_quality_data = {'CO': data['CO'], 'CO_ug_m3': data['CO_ug_m3'],'H2S': data['H2S'], 'H2S_ug_m3': data['H2S_ug_m3'],
                        'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'], 'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],
                        'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'], 'PM25': data['PM25'], 'PM10': data['PM10'], 
                        'lat': data['lat'],'lon': data['lon'], 'alt': data['alt'], 'timestamp_zone': data['timestamp'], 
                        'uv':data['UV'],'spl':data['SPL'], 'humidity':data['humidity'],'pressure':data['pressure'],
                        'temperature':data['temperature']}

    air_quality_measurement = AirQualityMeasurement(**air_quality_data, qhawax_id=qhawax_id)
    session.add(air_quality_measurement)
    session.commit()


def getTimeQhawaxHistory(installation_id):
    values= session.query(QhawaxInstallationHistory.last_time_physically_turn_on_zone, \
                          QhawaxInstallationHistory.last_registration_time_zone).\
                          filter(QhawaxInstallationHistory.id == installation_id).first()
    if (values!=None):
        return values
    else:
        return None

def queryDBGasAverageMeasurement(qhawax_name, gas_name, values_list):
    """
    Helper function to get gas average measurement

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type gas_name: string
    :param gas_name: gas or dust name

    :type values_list: array
    :param values_list: array of last time on and last time registration

    """
    qhawax_id = same_helper.getQhawaxID(qhawax_name)

    initial_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
    last_timestamp = datetime.datetime.now(dateutil.tz.tzutc()) - datetime.timedelta(hours=24)

    if(gas_name=='CO'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.CO.label('sensor'))
    elif(gas_name=='H2S'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.H2S.label('sensor'))
    elif(gas_name=='NO2'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.NO2.label('sensor'))
    elif(gas_name=='O3'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.O3.label('sensor'))
    elif(gas_name=='PM25'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.PM25.label('sensor'))
    elif(gas_name=='PM10'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.PM10.label('sensor'))
    elif(gas_name=='SO2'):
        sensors = (AirQualityMeasurement.timestamp_zone, AirQualityMeasurement.SO2.label('sensor'))

    last_time_turn_on = values_list['last_time_on']
    last_registration_time = values_list['last_time_registration']

    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                               filter(AirQualityMeasurement.timestamp_zone >= last_timestamp). \
                               filter(AirQualityMeasurement.timestamp_zone <= initial_timestamp). \
                               order_by(AirQualityMeasurement.timestamp_zone.asc()).all()

def qhawaxBelongsCompany(qhawax_id,company_id):
    """
    Helper function to valid if qHAWAX belongs to company

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type company_id: integer
    :param company_id: company ID

    """
    company_id_result = session.query(QhawaxInstallationHistory.company_id).filter(QhawaxInstallationHistory.qhawax_id == qhawax_id). \
                                       filter(QhawaxInstallationHistory.end_date_zone == None).first()[0]
    if(int(company_id_result)==int(company_id)):
        return True
    else:
        return False

def queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp):
    """
    Helper function to get Air Quality measurement

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type initial_timestamp: timestamp with time zone
    :param initial_timestamp: initial date with time

    type final_timestamp: timestamp with time zone
    :param final_timestamp: final date with time

    """
    sensors = (AirQualityMeasurement.CO_ug_m3, AirQualityMeasurement.H2S_ug_m3, AirQualityMeasurement.NO2_ug_m3,
                AirQualityMeasurement.O3_ug_m3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                AirQualityMeasurement.SO2_ug_m3, AirQualityMeasurement.uv,AirQualityMeasurement.uva, 
                AirQualityMeasurement.uvb, AirQualityMeasurement.spl,AirQualityMeasurement.humidity, 
                AirQualityMeasurement.pressure, AirQualityMeasurement.temperature, AirQualityMeasurement.lat, 
                AirQualityMeasurement.lon, AirQualityMeasurement.timestamp_zone)
    
    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                    filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp). \
                                    filter(AirQualityMeasurement.timestamp_zone <= final_timestamp). \
                                    order_by(AirQualityMeasurement.timestamp).all()

def storeGasIncaInDB(data):
    """
    Helper function to record GAS INCA measurement

    :type data: json
    :param data: gas inca measurement

    """
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_data = {'CO': data['CO'], 'H2S': data['H2S'], 'SO2': data['SO2'], 'NO2': data['NO2'],'O3': data['O3'],
             'PM25': data['PM25'], 'PM10': data['PM10'],'timestamp_zone': data['timestamp'],'main_inca':data['main_inca']}
    gas_inca_processed = GasInca(**gas_inca_data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()

def queryDBGasInca(initial_timestamp, final_timestamp):
    """
    Helper function to get GAS INCA measurement

    :type initial_timestamp: timestamp with time zone
    :param initial_timestamp: initial date with time

    type final_timestamp: timestamp with time zone
    :param final_timestamp: final date with time

    """
    sensors = (GasInca.CO, GasInca.H2S, GasInca.SO2, GasInca.NO2,GasInca.O3, 
                GasInca.PM25, GasInca.PM10, GasInca.SO2,GasInca.timestamp_zone, GasInca.qhawax_id, GasInca.main_inca)
    
    return session.query(*sensors).filter(GasInca.timestamp_zone >= initial_timestamp). \
                                    filter(GasInca.timestamp_zone <= final_timestamp).all()
                                  

def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)

    sensors = (ProcessedMeasurement.CO, ProcessedMeasurement.CO2, ProcessedMeasurement.H2S, ProcessedMeasurement.NO,
                ProcessedMeasurement.NO2, ProcessedMeasurement.O3, ProcessedMeasurement.PM1, ProcessedMeasurement.PM25,
                ProcessedMeasurement.PM10, ProcessedMeasurement.SO2, ProcessedMeasurement.VOC, ProcessedMeasurement.UV,
                ProcessedMeasurement.UVA, ProcessedMeasurement.UVB, ProcessedMeasurement.spl, ProcessedMeasurement.humidity,
                ProcessedMeasurement.pressure, ProcessedMeasurement.temperature, ProcessedMeasurement.lat,
                ProcessedMeasurement.lon, ProcessedMeasurement.alt, ProcessedMeasurement.timestamp_zone)

    return session.query(*sensors).filter(ProcessedMeasurement.qhawax_id == qhawax_id). \
                                    filter(ProcessedMeasurement.timestamp_zone > initial_timestamp). \
                                    filter(ProcessedMeasurement.timestamp_zone < final_timestamp). \
                                    order_by(ProcessedMeasurement.timestamp).all()

def storeProcessedDataInDB(data):
    """
    Helper Processed Measurement function to store Processed Data

    :type data: json
    :param data: Processed Measurement detail

    """
    qhawax_name = data.pop('ID', None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()

def getNoiseData(qhawax_name):
    """
    Helper Processed Measurement function to get Noise Area Description

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    eca_noise_id = session.query(QhawaxInstallationHistory.eca_noise_id).\
                           filter_by(qhawax_id=qhawax_id,end_date_zone=None).first()
    zone = session.query(EcaNoise.area_name).filter_by(id=eca_noise_id).first()[0]
    return zone

def getHoursDifference(qhawax_id):
    """
    Helper Processed Measurement function to get difference between last_registration_time and last_time_physically_turn_on

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    values = session.query(QhawaxInstallationHistory.last_time_physically_turn_on_zone, \
                           QhawaxInstallationHistory.last_registration_time_zone).\
                     filter(QhawaxInstallationHistory.qhawax_id == qhawax_id).first()
    if (values[0]!=None and values[1]!=None):
        minutes_difference = int((values[0] - values[1]).total_seconds() / 60)
        return minutes_difference, values[0]
    else:
        return None, None

def storeValidProcessedDataInDB(data, qhawax_id, product_id):
    """
    Helper Processed Measurement function to insert Valid Processed Data

    :type data: json
    :param data: Valid Processed Measurement detail

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type product_id: string
    :param product_id: qHAWAX name

    """
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id!=None):
        valid_data = {'timestamp_zone': data['timestamp'],'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'], 
                      'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'],
                      'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],
                      'PM25': data['PM25'],'lat':data['lat'],'lon':data['lon'],'PM1': data['PM1'],'PM10': data['PM10'],
                      'UV': data['UV'],'UVA': data['UVA'],'UVB': data['UVB'],'SPL': data['spl'],
                      'humidity': data['humidity'],'pressure': data['pressure'],'temperature': data['temperature']}
        valid_processed_measurement = ValidProcessedMeasurement(**valid_data, qhawax_installation_id=installation_id)
        session.add(valid_processed_measurement)
        session.commit()
        socketio.emit('new_data_summary_valid', data)              

def queryDBValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp):
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,
               ValidProcessedMeasurement.H2S_ug_m3,ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3, 
               ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, ValidProcessedMeasurement.PM25,
               ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
               ValidProcessedMeasurement.UV, ValidProcessedMeasurement.UVA,ValidProcessedMeasurement.UVB,
               ValidProcessedMeasurement.SPL, ValidProcessedMeasurement.humidity,ValidProcessedMeasurement.pressure, 
               ValidProcessedMeasurement.temperature, ValidProcessedMeasurement.lat,ValidProcessedMeasurement.lon, 
               ValidProcessedMeasurement.timestamp_zone)

    valid_measurement_list =session.query(*sensors).\
                                    filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                    filter(ValidProcessedMeasurement.timestamp_zone >= initial_timestamp). \
                                    filter(ValidProcessedMeasurement.timestamp_zone <= final_timestamp). \
                                    order_by(ValidProcessedMeasurement.timestamp_zone).all()
    return valid_measurement_list

def getLatestTimestampValidProcessed(qhawax_name):
    installation_id=same_helper.getInstallationIdBaseName(qhawax_name)
    time_valid_data = session.query(ValidProcessedMeasurement.timestamp_zone).\
                              filter_by(qhawax_installation_id=installation_id).first()
    valid_measurement_timestamp=""
    valid_processed_measurement_timestamp = []
    if(time_valid_data!=None):
        valid_processed_measurement_timestamp = session.query(ValidProcessedMeasurement.timestamp_zone).\
                                                        filter_by(qhawax_installation_id=installation_id). \
                                                        order_by(ValidProcessedMeasurement.id.desc()).first().timestamp_zone
    return valid_processed_measurement_timestamp

def queryDBDailyValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp):
    """
    Helper Valid Processed Measurement function to valid measurement filter by time

    :type installation_id: integer
    :param installation_id: qHAWAX Installation ID

    :type initial_timestamp: timestamp
    :param initial_timestamp: start date

    :type final_timestamp: timestamp
    :param final_timestamp: end date

    """
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,
               ValidProcessedMeasurement.H2S_ug_m3,ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3,
               ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, ValidProcessedMeasurement.PM25,
               ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
               ValidProcessedMeasurement.humidity,ValidProcessedMeasurement.pressure, ValidProcessedMeasurement.temperature, 
               ValidProcessedMeasurement.timestamp_zone)

    daily_valid_measurement_list =session.query(*sensors). \
                                          filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                          filter(ValidProcessedMeasurement.timestamp_zone > initial_timestamp). \
                                          filter(ValidProcessedMeasurement.timestamp_zone < final_timestamp). \
                                          order_by(ValidProcessedMeasurement.timestamp_zone).all()
    return daily_valid_measurement_list

def validAndBeautyJsonValidProcessed(data_json,qhawax_id,product_id,inca_value):
    storeValidProcessedDataInDB(data_json, qhawax_id, product_id)
    if(inca_value==0.0):
        business_helper.updateMainIncaInDB(1,product_id)


