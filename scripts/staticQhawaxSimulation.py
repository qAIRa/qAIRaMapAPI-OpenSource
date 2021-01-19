import requests
import sys
import time
from datetime import timedelta
import dateutil.parser
import dateutil.tz
import datetime
import random

# BASE_URL = 'https://qairamapnapi.qairadrones.com/'
BASE_URL = 'http://0.0.0.0:5000/'
PROCESSED_MEASUREMENT= BASE_URL + '/api/dataProcessed/'


measurement_qhawax = {"ID":None,"timestamp":None,"lat":-12.132288,"lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,\
					  "O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,"PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,\
					  "temperature":23.0,"pressure":100629.10,"humidity":3}
#times = 10
sleep_time_seconds=int(sys.argv[3])
times_iterate= int(sys.argv[2])
if(len(sys.argv)==4):
	for index in range(times_iterate):
		measurement_qhawax["ID"]=sys.argv[1]
		measurement_qhawax["timestamp"]= str(datetime.datetime.now(dateutil.tz.tzutc()))
		measurement_qhawax["O3"]= random.randrange(times_iterate)
		measurement_qhawax["H2S"]= random.randrange(times_iterate)
		measurement_qhawax["humidity"]= random.randrange(times_iterate-index)
		measurement_qhawax["UV"]= random.randrange(15)
		print(measurement_qhawax)
		response_measurement = requests.post(PROCESSED_MEASUREMENT, json=measurement_qhawax)
		time.sleep(sleep_time_seconds)