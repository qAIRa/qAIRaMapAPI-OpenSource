import requests
import time
import sys
import math
import dateutil.parser
import dateutil.tz
import datetime
import pytz
import random
from datetime import timedelta, tzinfo


# DATA_PROCESSED_ENDPOINT = 'api/dataProcessedMobile/'
# OPEN_BASE_URL = 'https://openqairamapnapi.qairadrones.com/'

BASE_URL = 'https://qairamapnapi.qairadrones.com/'
DATA_PROCESSED_TEST = 'api/dataProcessedTest/'

#PROCESSED_MEASUREMENT= OPEN_BASE_URL + DATA_PROCESSED_ENDPOINT
# produccion
PROCESSED_MEASUREMENT = BASE_URL + DATA_PROCESSED_TEST
print(PROCESSED_MEASUREMENT)
print('https://qairamapnapi.qairadrones.com/api/dataProcessedTest/')
# CO, CO2, NO2, O3, SO2, H2S, PM25, PM10, VOC  ug_m3

#"2021-05-26 12:20:00-05:00"
#'2021-05-26 17:19:15.560919+00:00'

data_json = {"CO": 10000,"CO_ug_m3": 8000,
              "H2S_ug_m3": 43.404,"H2S": 43.404,
              "NO2": 100.78,"NO2_ug_m3": 19.78,
              "O3": 40.126,"O3_ug_m3": 3.126,"VOC":0,
              "CO2":1,"SO2": 4.388,"SO2_ug_m3": 4.388,
              "PM10": 35.349,"PM25": 11.678,"UVA":1,
              "UVB":1,"alt": 0.0,"lat": -12.0402780000002,
              "lon": -77.0436090000003,"PM1":1,
              "timestamp": "2021-05-19 07:56:08-05:00",
              "ID":"qH022","pressure":10,"humidity":25,
              "I_temperature":25,"temperature":21,"spl":1,"UV":1}

times_iterate= int(sys.argv[1])
sleep_time_seconds=int(sys.argv[2])
offset =int(sys.argv[3])
R=6378137
dLat = offset/R

# def timestampLocal(time_zone,location_time_zone):
#     #datetime_timestamp= datetime.datetime.strptime(data_json['timestamp'], '%Y-%m-%d %H:%M:%S%z') #lo pasamos a utc 00
#     local_time = (datetime.datetime.now() + datetime.timedelta(hours=time_zone)).replace(microsecond=0)
#     loc_dt = location_time_zone.localize(local_time)
#     return loc_dt


if(len(sys.argv)==4):
   for index in range(times_iterate):
      now = datetime.datetime.now(dateutil.tz.tzutc())
      data_json['timestamp'] = str(now.replace(tzinfo=pytz.utc,microsecond=0))
      #data_json['timestamp_zone'] = str(datetime.datetime.now() + datetime.timedelta(hours=5))

      lat = data_json["lat"]
      lon = data_json["lon"]
      dLon = offset/(R*math.cos(math.pi*lat/180))
      data_json["lat"]= float(lat)+dLat*180/math.pi
      data_json["lon"]= float(lon)+dLon*180/math.pi

      data_json["CO_ug_m3"] = random.randrange(times_iterate)
      data_json["CO2"] = random.randrange(times_iterate)
      data_json["humidity"]= random.randrange(times_iterate-index)
      data_json["UV"]= random.randrange(15)

      print(" ")
      print(data_json)
      print(" ")
      response = requests.post(PROCESSED_MEASUREMENT, json=data_json)
      print(response.text)
   
