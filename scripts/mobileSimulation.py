import datetime
import math
import random
import sys
import time
from datetime import date, timedelta, tzinfo

import dateutil.parser
import dateutil.tz
import pytz
import requests

############# DON'T RUN THIS PLEASE, THANK YOU :)  ######################

# "2021-05-26 12:20:00-05:00"
#'2021-05-26 17:19:15.560919+00:00'

data_json = {
    "CO": 10000,
    "CO_ug_m3": 8000,
    "H2S_ug_m3": 43.404,
    "H2S": 43.404,
    "NO2": 100.78,
    "NO2_ug_m3": 19.78,
    "O3": 40.126,
    "O3_ug_m3": 3.126,
    "VOC": 0,
    "CO2": 1,
    "SO2": 4.388,
    "SO2_ug_m3": 4.388,
    "PM10": 35.349,
    "PM25": 11.678,
    "UVA": 1,
    "UVB": 1,
    "alt": 0.0,
    "lat": -12.0402780000002,
    "lon": -77.0436090000003,
    "PM1": 1,
    "timestamp": "2021-05-19 07:56:08-05:00",
    "ID": "qH022",
    "pressure": 10,
    "humidity": 25,
    "I_temperature": 25,
    "temperature": 21,
    "spl": 1,
    "UV": 1,
}

# jsonData = {'timestamp': data['timestamp'],
#             'CO': data['CO'],'CO_ug_m3': data['CO_ug_m3'],
#             'H2S': data['H2S'],'H2S_ug_m3': data['H2S_ug_m3'],
#             'SO2': data['SO2'],'SO2_ug_m3': data['SO2_ug_m3'],
#             'NO2': data['NO2'],'NO2_ug_m3': data['NO2_ug_m3'],
#             'O3': data['O3'],'O3_ug_m3': data['O3_ug_m3'],
#             'PM25': data['PM25'],'lat':data['lat'],'lon':data['lon'],
#             'PM1': data['PM1'],'PM10': data['PM10'], 'UV': data['UV'],
#             'UVA': data['UVA'],'UVB': data['UVB'],'SPL': data['spl'],
#             'humidity': data['humidity'], 'CO2':data['CO2'],
#             'pressure': data['pressure'],'temperature': data['temperature'],
#             'timestamp_zone': data['timestamp_zone'],
#             'I_temperature':data['I_temperature'],'VOC':data['VOC']}


times_iterate = int(sys.argv[1])
sleep_time_seconds = int(sys.argv[2])
offset = int(sys.argv[3])
R = 6378137
dLat = offset / R

# def timestampLocal(time_zone,location_time_zone):
#     #datetime_timestamp= datetime.datetime.strptime(data_json['timestamp'], '%Y-%m-%d %H:%M:%S%z') #lo pasamos a utc 00
#     local_time = (datetime.datetime.now() + datetime.timedelta(hours=time_zone)).replace(microsecond=0)
#     loc_dt = location_time_zone.localize(local_time)
#     return loc_dt


if len(sys.argv) == 4:
    for index in range(times_iterate):
        # now = datetime.datetime.now(dateutil.tz.tzutc())
        # data_json['timestamp'] = str(now.replace(tzinfo=pytz.utc,microsecond=0))
        time_zone = float(0)
        local_time = (
            datetime.datetime.now() + datetime.timedelta(hours=time_zone)
        ).replace(microsecond=0)
        loc_dt = pytz.timezone("America/Lima").localize(local_time)
        # time_server = loc_dt + datetime.timedelta(hours=5)
        # print(str(loc_dt))
        data_json["timestamp"] = str(loc_dt)
        # data_json['timestamp_zone'] = str(datetime.datetime.now() + datetime.timedelta(hours=5))

        lat = data_json["lat"]
        lon = data_json["lon"]
        dLon = offset / (R * math.cos(math.pi * lat / 180))
        data_json["lat"] = float(lat) + dLat * 180 / math.pi
        data_json["lon"] = float(lon) + dLon * 180 / math.pi

        data_json["CO_ug_m3"] = random.randrange(times_iterate)
        data_json["CO2"] = random.randrange(times_iterate)
        data_json["humidity"] = random.randrange(times_iterate - index)
        data_json["UV"] = random.randrange(15)

        # PUNTO A: verificar que el 'timestamp' tenga como valor el formato
        # de la hora local en peru con -05:00 al final, visualizado en el terminal.
        # Ejem: 2021-05-26 14:26:31-05:00
        # Si no sale así, modificar la línea 58, que contiene la variable timezone
        # hasta que obtengas la hora local.

        print(" ")
        print(data_json)
        print(" ")

        # SOLO DESCOMENTAR EL POST CUANDO SE VERIFICO EL PUNTO A
        response = requests.post(PROCESSED_MEASUREMENT, json=data_json)
        print(response.text)
