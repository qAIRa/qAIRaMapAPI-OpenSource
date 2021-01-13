import requests
import time

BASE_URL = 'https://openqairamapnapi.qairadrones.com/'
PROCESSED_MEASUREMENT= BASE_URL + '/api/dataProcessed/'

positions =[ {"ID":"qH004","timestamp":"2020-12-10 18:19:02.0-05:00","lat":-12.132288,\
			  "lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,\
			  "PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,"temperature":23.0,"pressure":100629.10,"humidity":3},{\
			  "ID":"qH004","timestamp":"2020-12-10 18:19:06.0-05:00","lat":-12.132351,"lon":-77.027687,"CO":42.505,\
			  "H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.818,"PM25":12.816,"PM10":25.680,"UV":0,"UVA":0,"UVB":0,\
			  "spl":0,"temperature":23.0,"pressure":100622.10,"humidity":2},
			  {"ID":"qH004","timestamp":"2020-12-10 18:19:02.0-05:00","lat":-12.132288,\
			  "lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,\
			  "PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,"temperature":23.0,"pressure":100629.10,"humidity":3},{\
			  "ID":"qH004","timestamp":"2020-12-10 18:19:06.0-05:00","lat":-12.132351,"lon":-77.027687,"CO":42.505,\
			  "H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.818,"PM25":12.816,"PM10":25.680,"UV":0,"UVA":0,"UVB":0,\
			  "spl":0,"temperature":23.0,"pressure":100622.10,"humidity":2},
			  {"ID":"qH004","timestamp":"2020-12-10 18:19:02.0-05:00","lat":-12.132288,\
			  "lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,\
			  "PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,"temperature":23.0,"pressure":100629.10,"humidity":3},{\
			  "ID":"qH004","timestamp":"2020-12-10 18:19:06.0-05:00","lat":-12.132351,"lon":-77.027687,"CO":42.505,\
			  "H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.818,"PM25":12.816,"PM10":25.680,"UV":0,"UVA":0,"UVB":0,\
			  "spl":0,"temperature":23.0,"pressure":100622.10,"humidity":2},
			  {"ID":"qH004","timestamp":"2020-12-10 18:19:02.0-05:00","lat":-12.132288,\
			  "lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,\
			  "PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,"temperature":23.0,"pressure":100629.10,"humidity":3},{\
			  "ID":"qH004","timestamp":"2020-12-10 18:19:06.0-05:00","lat":-12.132351,"lon":-77.027687,"CO":42.505,\
			  "H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.818,"PM25":12.816,"PM10":25.680,"UV":0,"UVA":0,"UVB":0,\
			  "spl":0,"temperature":23.0,"pressure":100622.10,"humidity":2},
			  {"ID":"qH004","timestamp":"2020-12-10 18:19:02.0-05:00","lat":-12.132288,\
			  "lon":-77.027702,"CO":42.363,"H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.775,"PM25":12.631,\
			  "PM10":25.046,"UV":0,"UVA":0,"UVB":0,"spl":0,"temperature":23.0,"pressure":100629.10,"humidity":3},{\
			  "ID":"qH004","timestamp":"2020-12-10 18:19:06.0-05:00","lat":-12.132351,"lon":-77.027687,"CO":42.505,\
			  "H2S":0,"NO2":0,"O3":0,"SO2":0,"PM1":4.818,"PM25":12.816,"PM10":25.680,"UV":0,"UVA":0,"UVB":0,\
			  "spl":0,"temperature":23.0,"pressure":100622.10,"humidity":2}]

for pos in positions:
	response_measurement = requests.post(PROCESSED_MEASUREMENT, json=pos)
	time.sleep(3)



