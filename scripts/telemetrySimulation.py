import requests
import time
import sys
import random
import math

# python scripts/telemetrySimulation.py "qH006" 20 1 7


# BASE_URL = 'https://openqairamapnapi.qairadrones.com/'
BASE_URL = 'http://0.0.0.0:5000/'
SEND_TELEMETRY= BASE_URL + '/api/send_telemetry_andean_drone/'
COMPLETE_FLIGHT =BASE_URL +'/api/complete_flight'

telemetry_qhawax ={
				"token": "droneandino123",
				"room" :"qH006",
				"telemetry": {
					"lat": -12.0724959,
					"lon": -77.0823532,
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
    "flight_end": "2021-01-25 14:35:00",
    "qhawax_name": "qH006",
    "flight_detail": "Terrible flight",
    "location": {
        "lat": -12.2222,
        "lon": -77.3333
    }
}

R=6378137
sleep_time_seconds=int(sys.argv[3])
times_iterate= int(sys.argv[2])
offset =int(sys.argv[4])
dLat = offset/R

if(len(sys.argv)==5):
	for index in range(times_iterate):
		telemetry_qhawax["room"]=sys.argv[1]
		telemetry_qhawax["telemetry"]["alt"]= random.randrange(times_iterate)
		telemetry_qhawax["telemetry"]["voltage"]= random.randrange(times_iterate)
		telemetry_qhawax["telemetry"]["airspeed"]= random.randrange(times_iterate-index)
		lat = telemetry_qhawax["telemetry"]["lat"]
		lon = telemetry_qhawax["telemetry"]["lon"]
		dLon = offset/(R*math.cos(math.pi*lat/180))
		telemetry_qhawax["telemetry"]["lat"]= float(lat)+dLat*180/math.pi
		telemetry_qhawax["telemetry"]["lon"]= float(lon)+dLon*180/math.pi
		print(telemetry_qhawax)
		response_telemetry = requests.post(SEND_TELEMETRY, json=telemetry_qhawax)
		time.sleep(sleep_time_seconds)

	complete_flight['location']['lat']=telemetry_qhawax["telemetry"]["lat"]
	complete_flight['location']['lon']=telemetry_qhawax["telemetry"]["lon"]
	response_telemetry = requests.post(COMPLETE_FLIGHT, json=complete_flight)