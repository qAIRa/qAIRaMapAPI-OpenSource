import requests
import time
import sys
import random
import math
import dateutil.parser
import dateutil.tz
import datetime

# python scripts/droneSimulation.py "qH006" 20 1 7


# BASE_URL = 'https://openqairamapnapi.qairadrones.com/'
BASE_URL = 'http://0.0.0.0:5000/'
SEND_TELEMETRY= BASE_URL + '/api/send_telemetry_andean_drone/'
COMPLETE_FLIGHT =BASE_URL +'/api/complete_flight'
START_FLIGHT = BASE_URL + 'api/record_start_flight'
PROCESSED_MEASUREMENT= BASE_URL + '/api/dataProcessed/'

measurement_qhawax = {
	"ID":None,
	"timestamp":None,
	"lat": -12.07070,
	"lon": -77.08052,
	"CO":42.363,
	"H2S":0,
	"NO2":0,
	"O3":0,
	"SO2":0,
	"PM1":4.775,
	"PM25":12.631,
	"PM10":25.046,
	"UV":0,
	"UVA":0,
	"UVB":0,
	"spl":0,
	"temperature":23.0,
	"pressure":100629.10,
	"humidity":3
	}

telemetry_qhawax ={
				"token": "droneandino123",
				"room" :"qH006",
				"telemetry": {
					"lat": -12.07070,
					"lon": -77.08052,
					"alt": -0.05,
					"dist_home": 0.0,
					"airspeed": 0.02,
					"waypoint": None,
					"last_waypoint": False,
					"flight_mode": "MANUAL",
					"just_landed": False,
					"new_flight": False,
					"voltage": 12.59,
					"current": 0.0,
					"level": 100,
					"sonar_dist": None,
					"num_gps": 10,
					"fix_type": 6,
					"IRLOCK_status": False,
					"status_msg": "",
					"throttle": None,
					"rcout": None,
					"compass1": None,
					"compass2": None,
					"gps": None,
					"gps2": None,
					"vibrations": None,
					"ekf_status": None,
					"yaw": 358,
					"irlock": None
					}
				}

complete_flight = {
    "flight_end": str(datetime.datetime.now(dateutil.tz.tzutc())),
    "qhawax_name": "qH006",
    "flight_detail": "Terrible flight",
    "location": {
        "lat": -12.2222,
        "lon": -77.3333
    }
}

start_flight = {
    "flight_start": str(datetime.datetime.now(dateutil.tz.tzutc())),
    "qhawax_name": "qH006"
}

R=6378137
sleep_time_seconds=int(sys.argv[3])
times_iterate= int(sys.argv[2])
offset =int(sys.argv[4])
dLat = offset/R



if(len(sys.argv)==5):
	start_flight['qhawax_name']=sys.argv[1]
	print(start_flight)
	response_telemetry = requests.post(START_FLIGHT, json=start_flight)

	for index in range(times_iterate):
		measurement_qhawax["ID"]=sys.argv[1]
		measurement_qhawax["timestamp"]= str(datetime.datetime.now(dateutil.tz.tzutc()))
		measurement_qhawax["O3"]= random.randrange(times_iterate)
		measurement_qhawax["H2S"]= random.randrange(times_iterate)
		measurement_qhawax["humidity"]= random.randrange(times_iterate-index)
		measurement_qhawax["UV"]= random.randrange(15)
		lat = measurement_qhawax["lat"]
		lon = measurement_qhawax["lon"]
		dLon = offset/(R*math.cos(math.pi*lat/180))
		measurement_qhawax["lat"]= float(lat)+dLat*180/math.pi
		measurement_qhawax["lon"]= float(lon)+dLon*180/math.pi
		print(measurement_qhawax)
		response_measurement = requests.post(PROCESSED_MEASUREMENT, json=measurement_qhawax)
		telemetry_qhawax["room"]=sys.argv[1]
		telemetry_qhawax["telemetry"]["alt"]= random.randrange(times_iterate)
		telemetry_qhawax["telemetry"]["voltage"]= random.randrange(times_iterate)
		telemetry_qhawax["telemetry"]["airspeed"]= random.randrange(times_iterate-index)
		telemetry_qhawax["telemetry"]["lat"]= float(lat)+dLat*180/math.pi
		telemetry_qhawax["telemetry"]["lon"]= float(lon)+dLon*180/math.pi
		print(telemetry_qhawax)
		response_telemetry = requests.post(SEND_TELEMETRY, json=telemetry_qhawax)
		time.sleep(sleep_time_seconds)

	complete_flight['qhawax_name']=sys.argv[1]	
	complete_flight['location']['lat']=telemetry_qhawax["telemetry"]["lat"]
	complete_flight['location']['lon']=telemetry_qhawax["telemetry"]["lon"]
	print(complete_flight)
	response_telemetry = requests.post(COMPLETE_FLIGHT, json=complete_flight)