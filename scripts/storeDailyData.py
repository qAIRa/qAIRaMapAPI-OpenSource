import requests
import datetime
import dateutil.parser
import dateutil.tz
from math import log10
import json

#BASE_URL = 'https://qairamapnapi-dev-opensource.qairadrones.com/'
#BASE_URL = 'http://54.159.70.183/'
BASE_URL = 'http://0.0.0.0:5000/'
GET_ACTIVE_QHAWAX_IN_FIELD = 'api/get_qhawaxs_active_mode_customer/'
DAILY_VALID_PROCESSED_DATA_ENDPOINT = 'api/daily_valid_processed_measurements/'
AIR_QUALITY_DATA_ENDPOINT = 'api/air_daily_quality_measurements/'


def averageValidProcessedMeasurements(valid_processed_measurements, yesterday_start):
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
            averaged_value = sum(sensor_values_without_none)/len(sensor_values_without_none)
            average_valid_processed_measurement[sensor_name] = round(averaged_value, 3)

    average_valid_processed_measurement['timestamp_zone'] = str(yesterday_start)
    return average_valid_processed_measurement

# Request all qhawax
response = requests.get(BASE_URL + GET_ACTIVE_QHAWAX_IN_FIELD)
json_data = json.loads(response.text)

for qhawax in json_data:
    yesterday_start = (datetime.datetime.now().replace(hour=5,minute=0, second=0, microsecond=0) - datetime.timedelta(hours=24))
    yesterday_end = datetime.datetime.now().replace(hour=5,minute=0, second=0, microsecond=0)
    print('Processing daily data %s...' % (qhawax['name']))
    print(yesterday_start)
    print(yesterday_end)
    params = {'qhawax_id': qhawax['id'], 'initial_timestamp': yesterday_start, 'final_timestamp':yesterday_end}
    response = requests.get(BASE_URL + DAILY_VALID_PROCESSED_DATA_ENDPOINT, params=params)
    daily_valid_processed_measurements = response.json()
    if len(daily_valid_processed_measurements) == 0:
        continue
    average_processed_measurement = averageValidProcessedMeasurements(daily_valid_processed_measurements,yesterday_start)
    average_processed_measurement['ID'] = qhawax['name']
    # Store averaged processed data in db
    response = requests.post(BASE_URL + AIR_QUALITY_DATA_ENDPOINT, json=average_processed_measurement)
    print(response.text)


