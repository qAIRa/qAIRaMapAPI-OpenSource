import requests
import datetime
import dateutil.parser
import dateutil.tz
from math import log10

#BASE_URL = 'https://qairamapnapi-dev-opensource.qairadrones.com/'
#BASE_URL = 'http://54.159.70.183/'
BASE_URL = 'http://0.0.0.0:5000/'
GET_ACTIVE_QHAWAX_IN_FIELD = 'api/get_qhawaxs_active_mode_customer/'
VALID_PROCESSED_DATA_ENDPOINT = 'api/valid_processed_measurements/'
AIR_QUALITY_DATA_ENDPOINT = 'api/air_quality_measurements/'


def calculateSPLLogarithmAverage(sensor_values_without_none):
    total=0
    quantity= len(sensor_values_without_none)
    for value in sensor_values_without_none:
        value = value/10 #Dividir entre 10
        value = 10 ** value #Antilogaritmo 
        total+=value #Acumulando
    average_spl=total/quantity #Promedio
    apply_log=10*log10(average_spl) #Aplicando el logaritmo base 10 * 10
    return apply_log

def averageValidProcessedMeasurements(valid_processed_measurements):
    SKIP_KEYS = ['timestamp','timestamp_zone']
    
    average_valid_processed_measurement = {}
    for sensor_name in valid_processed_measurements[0]:
        if sensor_name in SKIP_KEYS:
            continue
        sensor_values = [measurement[sensor_name] for measurement in valid_processed_measurements]
        if all([value is None for value in sensor_values]):
            average_valid_processed_measurement[sensor_name] = None 
        else:
            sensor_values_without_none = [value for value in sensor_values if value is not None]
            if sensor_name not in ['SPL']:
                averaged_value = sum(sensor_values_without_none)/len(sensor_values_without_none)
                if sensor_name not in ['lat','lon']:
                    average_valid_processed_measurement[sensor_name] = round(averaged_value, 3)
                else:
                    average_valid_processed_measurement[sensor_name] = averaged_value
            elif sensor_name in ['SPL']:
                #Para el caso del spl se tiene que obtener promedio logaritmico, no aritmetico
                average_valid_processed_measurement[sensor_name]= round(calculateSPLLogarithmAverage(sensor_values_without_none),3)
                  
    starting_hour = datetime.datetime.now(dateutil.tz.tzutc())
    average_valid_processed_measurement['timestamp_zone'] = str(starting_hour.replace(minute=0, second=0, microsecond=0))
    return average_valid_processed_measurement

# Request all qhawax
response = requests.get(BASE_URL + GET_ACTIVE_QHAWAX_IN_FIELD)
qhawax_names = [qhawax['name'] for qhawax in response.json()]

for qhawax_name in qhawax_names:
    print('Processing %s...' % (qhawax_name))
    params = {'name': qhawax_name, 'interval_hours': '1'}
    print("Antes del capturar data valid")
    response = requests.get(BASE_URL + VALID_PROCESSED_DATA_ENDPOINT, params=params)
    valid_processed_measurements = response.json()
    if len(valid_processed_measurements) == 0:
        continue
    print("Antes del promedio")
    average_processed_measurement = averageValidProcessedMeasurements(valid_processed_measurements)
    average_processed_measurement['ID'] = qhawax_name
    average_processed_measurement['alt'] = 0

    response = requests.post(BASE_URL + AIR_QUALITY_DATA_ENDPOINT, json=average_processed_measurement)
    print(response.text)


