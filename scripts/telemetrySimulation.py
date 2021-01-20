import requests
import time

BASE_URL = 'https://openqairamapnapi.qairadrones.com/'
SEND_TELEMETRY= BASE_URL + '/api/send_telemetry_andean_drone/'

positions =[{"token": "droneandino123", "room" :"qH008", "telemetry": {"lat": -12.0724959, "lon": -77.0823532,\
			 "alt": -0.05, "dist_home": 10.0, "airspeed": 0.02, "waypoint": null, "last_waypoint": false,\
			 "flight_mode": "MANUAL", "just_landed": false, "new_flight": false, "voltage": 10.59, "current": 0.0,\
			 "level": 100, "sonar_dist": null, "num_gps": 10, "fix_type": 6, "IRLOCK_status": false, "status_msg": "", \
			 "throttle": null, "rcout": null, "compass1": null, "compass2": null, "gps": null, "gps2": null, "vibrations": null,\
			 "ekf_status": null, "yaw": 358, "irlock": null}},
			 {"token": "droneandino123", "room" :"qH008", "telemetry": {"lat": -12.0824959, "lon": -77.0723532,\
			 "alt": -0.05, "dist_home": 5.0, "airspeed": 0.02, "waypoint": null, "last_waypoint": false,\
			 "flight_mode": "MANUAL", "just_landed": false, "new_flight": false, "voltage": 11.59, "current": 0.0,\
			 "level": 100, "sonar_dist": null, "num_gps": 10, "fix_type": 6, "IRLOCK_status": false, "status_msg": "", \
			 "throttle": null, "rcout": null, "compass1": null, "compass2": null, "gps": null, "gps2": null, "vibrations": null,\
			 "ekf_status": null, "yaw": 358, "irlock": null}},
			 {"token": "droneandino123", "room" :"qH008", "telemetry": {"lat": -12.0924959, "lon": -77.0623532,\
			 "alt": -0.05, "dist_home": 0.0, "airspeed": 0.02, "waypoint": null, "last_waypoint": false,\
			 "flight_mode": "MANUAL", "just_landed": false, "new_flight": false, "voltage": 12.59, "current": 0.0,\
			 "level": 100, "sonar_dist": null, "num_gps": 10, "fix_type": 6, "IRLOCK_status": false, "status_msg": "", \
			 "throttle": null, "rcout": null, "compass1": null, "compass2": null, "gps": null, "gps2": null, "vibrations": null,\
			 "ekf_status": null, "yaw": 358, "irlock": null}}]

for pos in positions:
	response_telemetry = requests.post(SEND_TELEMETRY, json=pos)
	time.sleep(3)