import datetime
import dateutil
import dateutil.parser
import time
from project import app, db, socketio

from project.database.models import AirQualityMeasurement, ProcessedMeasurement, GasInca, ValidProcessedMeasurement, Qhawax, QhawaxInstallationHistory, EcaNoise,AirDailyMeasurement

from project.database.utils import Location

elapsed_time = None
data_storage = []
qhawax_storage = {}
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
MAX_SECONDS_DATA_STORAGE = 30
MAX_LEN_DATA_STORAGE = 30
pollutant=['SO2','NO2','O3','CO','H2S']
pollutant_15C=[2.71,1.95,2.03,1.18,1.44]
pollutant_20C=[2.66,1.91,2.00,1.16,1.41]
pollutant_25C=[2.62,1.88,1.96,1.15,1.39]

session = db.session

def queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None

    sensors = (AirQualityMeasurement.CO, AirQualityMeasurement.H2S, AirQualityMeasurement.NO2,
                AirQualityMeasurement.O3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                AirQualityMeasurement.SO2, AirQualityMeasurement.lat, AirQualityMeasurement.lon, 
                AirQualityMeasurement.alt, AirQualityMeasurement.timestamp)
    
    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                    filter(AirQualityMeasurement.timestamp >= initial_timestamp). \
                                    filter(AirQualityMeasurement.timestamp <= final_timestamp). \
                                    order_by(AirQualityMeasurement.timestamp).all()

#$ esto es del script
def storeAirQualityDataInDB(data):
    qhawax_name = data.pop('ID', None)
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    
    air_quality_data = {'CO': data['CO'], 'CO_ug_m3': data['CO_ug_m3'],'H2S': data['H2S'], 'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],
                        'SO2_ug_m3': data['SO2_ug_m3'], 'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'], 
                        'PM25': data['PM25'], 'PM10': data['PM10'], 'lat': data['lat'],'lon': data['lon'], 'alt': data['alt'], 
                        'timestamp': data['timestamp'], 'uv':data['UV'],'spl':data['SPL'], 'humidity':data['humidity'],
                        'pressure':data['pressure'],'temperature':data['temperature']}

    air_quality_measurement = AirQualityMeasurement(**air_quality_data, qhawax_id=qhawax_id)
    session.add(air_quality_measurement)
    session.commit()


def queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None

    sensors = (AirQualityMeasurement.CO, AirQualityMeasurement.H2S, AirQualityMeasurement.NO2,
                AirQualityMeasurement.O3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                AirQualityMeasurement.SO2, AirQualityMeasurement.lat, AirQualityMeasurement.lon, 
                AirQualityMeasurement.alt, AirQualityMeasurement.timestamp)
    
    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                    filter(AirQualityMeasurement.timestamp >= initial_timestamp). \
                                    filter(AirQualityMeasurement.timestamp <= final_timestamp). \
                                    order_by(AirQualityMeasurement.timestamp).all()


def getInstallationIdBaseName(qhawax_name):
    qhawax_id = session.query(Qhawax.id).filter(Qhawax.name == qhawax_name).one()
    installation_id = getInstallationId(qhawax_id)
    return installation_id


def getTimeQhawaxHistory(installation_id):
    values= session.query(QhawaxInstallationHistory.last_time_physically_turn_on, QhawaxInstallationHistory.last_registration_time).filter(QhawaxInstallationHistory.id == installation_id).first()
    if (values!=None):
        return values
    else:
        return None

#$
def queryDBGasAverageMeasurement(qhawax_name, gas_name, values_list):
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None

    initial_timestamp = datetime.datetime.now()- datetime.timedelta(hours=5)
    last_timestamp = datetime.datetime.now() - datetime.timedelta(hours=29)

    if(gas_name=='CO'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.CO.label('sensor'))
    elif(gas_name=='H2S'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.H2S.label('sensor'))
    elif(gas_name=='NO2'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.NO2.label('sensor'))
    elif(gas_name=='O3'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.O3.label('sensor'))
    elif(gas_name=='PM25'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.PM25.label('sensor'))
    elif(gas_name=='PM10'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.PM10.label('sensor'))
    elif(gas_name=='SO2'):
        sensors = (AirQualityMeasurement.timestamp, AirQualityMeasurement.SO2.label('sensor'))

    last_time_turn_on = values_list['last_time_on']
    last_registration_time = values_list['last_time_registration']

    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                               filter(AirQualityMeasurement.timestamp >= last_timestamp). \
                               filter(AirQualityMeasurement.timestamp <= initial_timestamp). \
                               order_by(AirQualityMeasurement.timestamp.asc()).all()

def qhawaxBelongsCompany(qhawax_id,company_id):
    company_id_result = session.query(QhawaxInstallationHistory.company_id).filter(QhawaxInstallationHistory.qhawax_id == qhawax_id). \
                                       filter(QhawaxInstallationHistory.end_date == None).first()[0]
    if(int(company_id_result)==int(company_id)):
        return True
    else:
        return False

def queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp):
    sensors = (AirQualityMeasurement.CO_ug_m3, AirQualityMeasurement.H2S_ug_m3, AirQualityMeasurement.NO2_ug_m3,
                AirQualityMeasurement.O3_ug_m3, AirQualityMeasurement.PM25, AirQualityMeasurement.PM10, 
                AirQualityMeasurement.SO2_ug_m3, AirQualityMeasurement.uv,AirQualityMeasurement.uva, 
                AirQualityMeasurement.uvb, AirQualityMeasurement.spl,AirQualityMeasurement.humidity, 
                AirQualityMeasurement.pressure, AirQualityMeasurement.temperature, AirQualityMeasurement.lat, 
                AirQualityMeasurement.lon, AirQualityMeasurement.timestamp)
    
    return session.query(*sensors).filter(AirQualityMeasurement.qhawax_id == qhawax_id). \
                                    filter(AirQualityMeasurement.timestamp >= initial_timestamp). \
                                    filter(AirQualityMeasurement.timestamp <= final_timestamp). \
                                    order_by(AirQualityMeasurement.timestamp).all()

def storeGasIncaInDB(data):
    qhawax_name = data.pop('ID', None)
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    gas_inca_data = {'CO': data['CO'], 'H2S': data['H2S'], 'SO2': data['SO2'], 'NO2': data['NO2'],'O3': data['O3'],
             'PM25': data['PM25'], 'PM10': data['PM10'],'timestamp': data['timestamp'],'main_inca':data['main_inca']}
    gas_inca_processed = GasInca(**gas_inca_data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()

def queryDBGasInca(initial_timestamp, final_timestamp):
    sensors = (GasInca.CO, GasInca.H2S, GasInca.SO2, GasInca.NO2,GasInca.O3, 
                GasInca.PM25, GasInca.PM10, GasInca.SO2,GasInca.timestamp, GasInca.qhawax_id, GasInca.main_inca)
    
    return session.query(*sensors).filter(GasInca.timestamp >= initial_timestamp). \
                                    filter(GasInca.timestamp <= final_timestamp).all()

def getQhawaxName(qhawax_id):
    return session.query(Qhawax.name).filter(Qhawax.id == qhawax_id).one()                                     

def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None

    sensors = (ProcessedMeasurement.CO, ProcessedMeasurement.CO2, ProcessedMeasurement.H2S, ProcessedMeasurement.NO,
                ProcessedMeasurement.NO2, ProcessedMeasurement.O3, ProcessedMeasurement.PM1, ProcessedMeasurement.PM25,
                ProcessedMeasurement.PM10, ProcessedMeasurement.SO2, ProcessedMeasurement.VOC, ProcessedMeasurement.UV,
                ProcessedMeasurement.UVA, ProcessedMeasurement.UVB, ProcessedMeasurement.spl, ProcessedMeasurement.humidity,
                ProcessedMeasurement.pressure, ProcessedMeasurement.temperature, ProcessedMeasurement.lat,
                ProcessedMeasurement.lon, ProcessedMeasurement.alt, ProcessedMeasurement.timestamp)

    return session.query(*sensors).filter(ProcessedMeasurement.qhawax_id == qhawax_id). \
                                    filter(ProcessedMeasurement.timestamp > initial_timestamp). \
                                    filter(ProcessedMeasurement.timestamp < final_timestamp). \
                                    order_by(ProcessedMeasurement.timestamp).all()

def gasConversionPPBtoMG(data_json,season):
    data={'ID': data_json['ID'],'CO': data_json['CO'], 'CO_ug_m3': 0,'H2S': data_json['H2S'],'H2S_ug_m3': 0,'NO2': data_json['NO2'],'NO2_ug_m3': 0,'O3': data_json['O3'],
                'O3_ug_m3': 0, 'PM1': data_json['PM1'],'PM10': data_json['PM10'],'PM25': data_json['PM25'],'SO2': data_json['SO2'],'SO2_ug_m3': 0,'spl': data_json['spl'],
                'UV': data_json['UV'],'UVA': data_json['UVA'],'UVB': data_json['UVB'],'humidity': data_json['humidity'],'lat':data_json['lat'],
                'lon':data_json['lon'],'pressure': data_json['pressure'],'temperature': data_json['temperature'],'timestamp': data_json['timestamp']}
    for key in data:
        if(key in pollutant):
            if(key=='SO2'):
                data['SO2_ug_m3']=data[key]*season[0]
            elif(key=='NO2'):
                data['NO2_ug_m3']=data[key]*season[1]
            elif(key=='O3'):
                data['O3_ug_m3']=data[key]*season[2]
            elif(key=='CO'):
                data['CO_ug_m3']=data[key]*season[3]
            elif(key=='H2S'):
                data['H2S_ug_m3']=data[key]*season[4]
    return data


def roundUpThree(data_json):
    data_json['CO']= round(data_json['CO'],3)
    data_json['CO_ug_m3']= round(data_json['CO_ug_m3'],3)
    data_json['H2S']= round(data_json['H2S'],3)
    data_json['H2S_ug_m3']= round(data_json['H2S_ug_m3'],3)
    data_json['NO2']= round(data_json['NO2'],3)
    data_json['NO2_ug_m3']= round(data_json['NO2_ug_m3'],3)
    data_json['O3']= round(data_json['O3'],3)
    data_json['O3_ug_m3']= round(data_json['O3_ug_m3'],3)
    data_json['PM1']= round(data_json['PM1'],3)
    data_json['PM10']= round(data_json['PM10'],3)
    data_json['PM25']= round(data_json['PM25'],3)
    data_json['SO2']= round(data_json['SO2'],3)
    data_json['SO2_ug_m3']= round(data_json['SO2_ug_m3'],3)
    data_json['spl']= round(data_json['spl'],3)
    data_json['UV']= round(data_json['UV'],3)
    data_json['humidity']= round(data_json['humidity'],3)
    data_json['pressure']= round(data_json['pressure'],3)
    return data_json

def storeProcessedDataInDB(data):
    """
    Helper Processed Measurement function to store Processed Data

    :type data: json
    :param data: Processed Measurement detail

    """
    qhawax_name = data.pop('ID', None)
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()

def getQhawaxId(qhawax_name):
    """
    Helper Processed Measurement function to get qHAWAX ID

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    return qhawax_id

def getNoiseData(qhawax_name):
    """
    Helper Processed Measurement function to get Noise Area Description

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    eca_noise_id = session.query(QhawaxInstallationHistory.eca_noise_id).filter_by(qhawax_id=qhawax_id,end_date=None).first()
    zone = session.query(EcaNoise.area_name).filter_by(id=eca_noise_id).first()[0]
    return zone

def getHoursDifference(qhawax_id):
    """
    Helper Processed Measurement function to get difference between last_registration_time and last_time_physically_turn_on

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    values = session.query(QhawaxInstallationHistory.last_time_physically_turn_on, QhawaxInstallationHistory.last_registration_time).filter(QhawaxInstallationHistory.qhawax_id == qhawax_id).first()
    if (values[0]!=None and values[1]!=None):
        minutes_difference = int((values[0] - values[1]).total_seconds() / 60)
        return minutes_difference, values[0]
    else:
        return None, None

def getMainIncaQhawaxTable(name):
    """
    Helper Processed Measurement function to get Main Inca from qHAWAX Table

    :type name: string
    :param name: qHAWAX name

    """
    qhawax_inca = ""
    if(isinstance(name, str)):
        qhawax_inca = session.query(Qhawax.main_inca).filter_by(name=name).all()
        if(qhawax_inca == []):
            raise TypeError("The qHAWAX name was not found")
        qhawax_inca = session.query(Qhawax.main_inca).filter_by(name=name).one()[0]
    else:
        raise TypeError("The qHAWAX name should be string")
    return qhawax_inca

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
    installation_id = getInstallationId(qhawax_id)
    if(installation_id!=None):
        valid_data = {'timestamp': data['timestamp'],'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'], 'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],
                    'SO2_ug_m3': data['SO2_ug_m3'],'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],'PM25': data['PM25'],
                    'lat':data['lat'],'lon':data['lon'],'PM1': data['PM1'],'PM10': data['PM10'],'UV': data['UV'],'UVA': data['UVA'],'UVB': data['UVB'],
                    'SPL': data['spl'],'humidity': data['humidity'],'pressure': data['pressure'],'temperature': data['temperature']}
        valid_processed_measurement = ValidProcessedMeasurement(**valid_data, qhawax_installation_id=installation_id)
        session.add(valid_processed_measurement)
        session.commit()
        socketio.emit('new_data_summary_valid', data)


def queryDBProcessedByQhawaxByCompany(qhawax_id, initial_timestamp, final_timestamp):
    sensors = (ProcessedMeasurement.CO, ProcessedMeasurement.CO2, ProcessedMeasurement.H2S, ProcessedMeasurement.NO,
                ProcessedMeasurement.NO2, ProcessedMeasurement.O3, ProcessedMeasurement.PM1, ProcessedMeasurement.PM25,
                ProcessedMeasurement.PM10, ProcessedMeasurement.SO2, ProcessedMeasurement.VOC, ProcessedMeasurement.UV,
                ProcessedMeasurement.UVA, ProcessedMeasurement.UVB, ProcessedMeasurement.spl, ProcessedMeasurement.humidity,
                ProcessedMeasurement.pressure, ProcessedMeasurement.temperature, ProcessedMeasurement.lat,
                ProcessedMeasurement.lon, ProcessedMeasurement.alt, ProcessedMeasurement.timestamp)

    measurement_list =session.query(*sensors).filter(ProcessedMeasurement.qhawax_id == int(qhawax_id)). \
                                    filter(ProcessedMeasurement.timestamp > initial_timestamp). \
                                    filter(ProcessedMeasurement.timestamp < final_timestamp). \
                                    order_by(ProcessedMeasurement.timestamp).all()
    return measurement_list

def handleTimestampInData(data):
    if 'timestamp' not in data:
        data['timestamp'] = datetime.datetime.now()
    else:
        data['timestamp'] = dateutil.parser.parse(data['timestamp'])
    return data

def storeRawDataInDB(data):
    global elapsed_time, data_storage, qhawax_storage
    if elapsed_time is None:
        elapsed_time = time.time()
    if time.time() - elapsed_time >= MAX_SECONDS_DATA_STORAGE or len(data_storage) >= MAX_LEN_DATA_STORAGE:
        for raw_measurement in data_storage:
            session.add(raw_measurement)
        session.commit()

        data_storage = []
        elapsed_time = time.time()  
    qhawax_name = data.pop('ID', None)
    if qhawax_name not in qhawax_storage:
        qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()
        qhawax_storage[qhawax_name] = qhawax_id[0]
    raw_measurement = RawMeasurement(**data, qhawax_id=qhawax_storage[qhawax_name])
    data_storage.append(raw_measurement)


def queryDBRaw(qhawax_name, initial_timestamp, final_timestamp):
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    if qhawax_id is None:
        return None

    sensors = (RawMeasurement.CO_OP1, RawMeasurement.CO_OP2, RawMeasurement.CO2, RawMeasurement.H2S_OP1, 
                RawMeasurement.H2S_OP2, RawMeasurement.NO_OP1, RawMeasurement.NO_OP2, RawMeasurement.NO2_OP1, 
                RawMeasurement.NO2_OP2, RawMeasurement.O3_OP1, RawMeasurement.O3_OP2, RawMeasurement.PM1, 
                RawMeasurement.PM25, RawMeasurement.PM10, RawMeasurement.SO2_OP1, RawMeasurement.SO2_OP2, 
                RawMeasurement.VOC_OP1, RawMeasurement.VOC_OP2, RawMeasurement.UV, RawMeasurement.UVA, 
                RawMeasurement.UVB, RawMeasurement.spl, RawMeasurement.humidity, RawMeasurement.pressure, 
                RawMeasurement.temperature, RawMeasurement.lat, RawMeasurement.lon, RawMeasurement.alt, 
                RawMeasurement.timestamp)
    return session.query(*sensors).filter(RawMeasurement.qhawax_id == qhawax_id). \
                                    filter(RawMeasurement.timestamp > initial_timestamp). \
                                    filter(RawMeasurement.timestamp < final_timestamp). \
                                    order_by(RawMeasurement.timestamp).all()

def getInstallationId(qhawax_id):
    installation_id = session.query(QhawaxInstallationHistory.id).filter_by(qhawax_id=qhawax_id). \
                                    filter(QhawaxInstallationHistory.end_date == None). \
                                    order_by(QhawaxInstallationHistory.instalation_date.desc()).first()[0]
    return installation_id                                   

def queryDBValidProcessedByQhawax(installation_id, initial_timestamp, final_timestamp):
    sensors = (ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S_ug_m3,
                ValidProcessedMeasurement.NO2_ug_m3, ValidProcessedMeasurement.O3_ug_m3, 
                ValidProcessedMeasurement.PM25,ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2_ug_m3,
                ValidProcessedMeasurement.UV, ValidProcessedMeasurement.SPL, ValidProcessedMeasurement.humidity,
                ValidProcessedMeasurement.pressure, ValidProcessedMeasurement.temperature, ValidProcessedMeasurement.lat,
                ValidProcessedMeasurement.lon, ValidProcessedMeasurement.timestamp)

    valid_measurement_list =session.query(*sensors).filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                    filter(ValidProcessedMeasurement.timestamp > initial_timestamp). \
                                    filter(ValidProcessedMeasurement.timestamp < final_timestamp). \
                                    order_by(ValidProcessedMeasurement.timestamp).all()
    return valid_measurement_list

def queryDBValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp):
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,ValidProcessedMeasurement.H2S_ug_m3,
                ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3, ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, 
                ValidProcessedMeasurement.PM25,ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
                ValidProcessedMeasurement.UV, ValidProcessedMeasurement.UVA,ValidProcessedMeasurement.UVB,ValidProcessedMeasurement.SPL, ValidProcessedMeasurement.humidity,
                ValidProcessedMeasurement.pressure, ValidProcessedMeasurement.temperature, ValidProcessedMeasurement.lat,
                ValidProcessedMeasurement.lon, ValidProcessedMeasurement.timestamp)

    valid_measurement_list =session.query(*sensors).filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                    filter(ValidProcessedMeasurement.timestamp > initial_timestamp). \
                                    filter(ValidProcessedMeasurement.timestamp < final_timestamp). \
                                    order_by(ValidProcessedMeasurement.timestamp).all()
    return valid_measurement_list

def getLatestTimestampValidProcessed(qhawax_name):
    installation_id=getInstallationIdBaseName(qhawax_name)
    time_valid_data = session.query(ValidProcessedMeasurement.timestamp).filter_by(qhawax_installation_id=installation_id).first()
    valid_measurement_timestamp=""
    if(time_valid_data!=None):
        valid_processed_measurement_timestamp = session.query(ValidProcessedMeasurement.timestamp).filter_by(qhawax_installation_id=installation_id) \
            .order_by(ValidProcessedMeasurement.id.desc()).first().timestamp
    return valid_processed_measurement_timestamp


def averageMeasurementsInHours(measurements, initial_timestamp, final_timestamp, interval_hours):
    initial_hour_utc = initial_timestamp.astimezone(tz=dateutil.tz.tzutc()).replace(tzinfo=None)
    final_hour_utc = final_timestamp.astimezone(tz=dateutil.tz.tzutc()).replace(tzinfo=None)
    initial_hour = initial_hour_utc.replace(minute=0, second=0, microsecond=0)
    final_hour = final_hour_utc.replace(minute=0, second=0, microsecond=0)

    current_hour = initial_hour
    ind = 0
    measurements_in_timestamp = []
    averaged_measurements = []
    while current_hour < final_hour:
        if ind > len(measurements) - 1:
            break
        
        timestamp = measurements[ind]['timestamp']
        if timestamp >= current_hour and timestamp <= current_hour + datetime.timedelta(hours=interval_hours):
            measurements_in_timestamp.append(measurements[ind])
            ind += 1
        else:
            if len(measurements_in_timestamp) != 0:
                averaged_measurement = averageMeasurements(measurements_in_timestamp)
                averaged_measurement['timestamp'] = current_hour
                averaged_measurements.append(averaged_measurement)
            measurements_in_timestamp = []
            current_hour += datetime.timedelta(hours=interval_hours)
    
    if len(measurements_in_timestamp) != 0:
        averaged_measurement = averageMeasurements(measurements_in_timestamp)
        averaged_measurement['timestamp'] = current_hour
        averaged_measurements.append(averaged_measurement)

    return averaged_measurements


def averageMeasurements(measurements):
    SKIP_KEYS = ['timestamp', 'lat', 'lon']

    average_measurement = {}

    for sensor_name in measurements[0]:
        if sensor_name in SKIP_KEYS:
            continue
        
        sensor_values = [measurement[sensor_name] for measurement in measurements]
        if all([value is None for value in sensor_values]):
            average_measurement[sensor_name] = None
        else:
            sensor_values_without_none = [value for value in sensor_values if value is not None]
            average_measurement[sensor_name] = sum(sensor_values_without_none)/len(sensor_values_without_none)

    average_measurement['timestamp'] = measurements[-1]['timestamp']
    average_measurement['lat'] = measurements[-1]['lat']
    average_measurement['lon'] = measurements[-1]['lon']

    return average_measurement


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
    sensors = (ValidProcessedMeasurement.CO, ValidProcessedMeasurement.CO_ug_m3,ValidProcessedMeasurement.H2S,ValidProcessedMeasurement.H2S_ug_m3,
                ValidProcessedMeasurement.NO2, ValidProcessedMeasurement.NO2_ug_m3, ValidProcessedMeasurement.O3,ValidProcessedMeasurement.O3_ug_m3, 
                ValidProcessedMeasurement.PM25,ValidProcessedMeasurement.PM10, ValidProcessedMeasurement.SO2,ValidProcessedMeasurement.SO2_ug_m3,
                ValidProcessedMeasurement.humidity,ValidProcessedMeasurement.pressure, ValidProcessedMeasurement.temperature, ValidProcessedMeasurement.timestamp)

    daily_valid_measurement_list =session.query(*sensors).filter(ValidProcessedMeasurement.qhawax_installation_id == int(installation_id)). \
                                    filter(ValidProcessedMeasurement.timestamp > initial_timestamp). \
                                    filter(ValidProcessedMeasurement.timestamp < final_timestamp). \
                                    order_by(ValidProcessedMeasurement.timestamp).all()
    return daily_valid_measurement_list

def storeAirDailyQualityDataInDB(data):
    """
    Helper Daily Air Measurement function to store air daily measurement

    :type data: json
    :param data: json of average of daily measurement

    """
    qhawax_name = data.pop('ID', None)
    qhawax_id = session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    
    air_daily_quality_data = {'CO': data['CO'], 'CO_ug_m3': data['CO_ug_m3'],'H2S': data['H2S'], 'H2S_ug_m3': data['H2S_ug_m3'],'SO2': data['SO2'],
                        'SO2_ug_m3': data['SO2_ug_m3'], 'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'], 
                        'PM25': data['PM25'], 'PM10': data['PM10'], 'timestamp': data['timestamp'], 'humidity':data['humidity'],
                        'pressure':data['pressure'],'temperature':data['temperature']}

    air_daily_quality_measurement = AirDailyMeasurement(**air_daily_quality_data, qhawax_id=qhawax_id)
    session.add(air_daily_quality_measurement)
    session.commit()

def getComercialName(qhawax_id):
    """
    Helper Processed Measurement function to get qHAWAX comercial name

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    if(isinstance(qhawax_id, int)):
        comercial_name = session.query(QhawaxInstallationHistory.comercial_name).filter_by(qhawax_id=qhawax_id, end_date=None).all()
        if(comercial_name == []):
            raise TypeError("The qHAWAX comercial name could not be found")
        comercial_name = session.query(QhawaxInstallationHistory.comercial_name).filter_by(qhawax_id=qhawax_id, end_date=None).one()[0]
    return comercial_name


def checkNegatives(data_json):
    """
    Helper Processed Measurement function to valid negatives values

    :type data_json: json
    :param data_json: json of measurement

    """
    if(data_json["temperature"]<0):
        data_json["temperature"] = 0

    if(data_json["pressure"]<0):
        data_json["pressure"] = 0

    if(data_json["humidity"]<0):
        data_json["humidity"] = 0

    if(data_json["spl"]<0):
        data_json["spl"] = 0

    if(data_json["UV"]<0):
        data_json["UV"] = 0

    if(data_json["UVA"]<0):
        data_json["UVA"] = 0

    if(data_json["UVB"]<0):
        data_json["UVB"] = 0

    if(data_json["CO"]<0):
        data_json["CO"] = 0

    if(data_json["H2S"]<0):
        data_json["H2S"] = 0

    if(data_json["NO2"]<0):
        data_json["NO2"] = 0

    if(data_json["O3"]<0):
        data_json["O3"] = 0

    if(data_json["SO2"]<0):
        data_json["SO2"] = 0

    if(data_json["PM1"]<0):
        data_json["PM1"] = 0

    if(data_json["PM25"]<0):
        data_json["PM25"] = 0

    if(data_json["PM10"]<0):
        data_json["PM10"] = 0

    return data_json


