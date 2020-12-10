import requests
import dateutil.parser
import datetime
from passlib.hash import bcrypt
import json
import os

ALLOWED_TIME_MINUTES = 2
BASE_URL = 'https://qairamapnapi.qairadrones.com/'
#BASE_URL = 'https://qairamapnapi-dev.qairadrones.com/'
#BASE_URL = 'http://0.0.0.0:5000/'

GET_ACTIVE_CUSTOMER_QHAWAX = BASE_URL + 'api/get_qhawaxs_active_mode_customer/'
GET_QHAWAX_TIMESTAMP_URL = BASE_URL + 'api/get_time_processed_data_active_qhawax/'
SET_QHAWAX_OFF =  BASE_URL + 'api/qhawax_change_status_off/'
SECRET_KEY = os.environ.get('SECRET_KEY')
ENV_TYPE = str(os.environ.get('ENV_TYPE'))

def isQhawaxLostActivity(qhawax_lost_activity_timestamp_str, now_timestamp):
    return (now_timestamp - qhawax_lost_activity_timestamp_str).total_seconds()/60 >= ALLOWED_TIME_MINUTES
all_active_qhawax_response=requests.get(GET_ACTIVE_CUSTOMER_QHAWAX)
json_data = json.loads(all_active_qhawax_response.text)
for qhawax in json_data:
	response_time = requests.get(GET_QHAWAX_TIMESTAMP_URL, params={'qhawax_name': qhawax['name']})
	if(response_time.text!="" and (response_time.text!='None')):
		qhawax_lost_timestamp_utc = dateutil.parser.parse(response_time.text)
		if isQhawaxLostActivity(qhawax_lost_timestamp_utc, datetime.datetime.now(dateutil.tz.tzutc())):
			qhawax_lost_timestamp = (qhawax_lost_timestamp_utc - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
			if(qhawax['main_inca']!=-1.0):
				print("Entre a apagar el qhawax: " + str(qhawax['name']))
				print("Ultima vez fue:  "+ str(qhawax_lost_timestamp))
				qhawax_lost_timestamp_utc = (qhawax_lost_timestamp_utc).strftime("%Y-%m-%d %H:%M:%S") 
				response_turn_off = requests.post(SET_QHAWAX_OFF, json={'qhawax_name':qhawax['name'],'qhawax_lost_timestamp':qhawax_lost_timestamp_utc })
				print(response_turn_off.text)
	else:
		print("No hay registros en el qhawax: " + qhawax['name'])

#Cambie bcrypt.encrypt(SECRET_KEY) por bcrypt.hash(SECRET_KEY)
