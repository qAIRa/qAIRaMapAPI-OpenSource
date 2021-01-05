import unittest
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import project.main.data.post_data_helper as post_data_helper
import pytz

class TestPostDataHelper(unittest.TestCase):
	""" Test of Post Data Functions """
	def test_store_air_quality_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,"String_")

	def test_store_air_quality_valid(self):
		air_quality_json= {"CO": 1986.208,"CO_ug_m3": 1986.208,"H2S_ug_m3": 43.404,"H2S": 43.404,
						   "NO2": 19.78,"NO2_ug_m3": 19.78,"O3": 3.126,"O3_ug_m3": 3.126,
						   "SO2": 4.388,"SO2_ug_m3": 4.388,"PM10": 35.349,"PM25": 11.678,
						   "alt": 0.0,"lat": -12.0402780000002,"lon": -77.0436090000003,
						   "timestamp_zone": "Fri, 01 Jan 2021 00:00:00 GMT", "ID":"qH057",
						   "pressure":10,"humidity":25,"I_temperature":25,"temperature":21,"SPL":1,"UV":1}
		post_data_helper.storeAirQualityDataInDB(air_quality_json)

	def test_store_gas_inca_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,"String_")

	def test_store_gas_inca_valid(self):
		gas_inca_json= {"CO": 1986.208,"H2S": 43.404,"NO2": 19.78,"O3": 3.126,"SO2": 4.388,"PM10": 35.349,"PM25": 11.678,"lat": -12.040278002,
						"lon": -77.0436003,"timestamp_zone": "Fri, 01 Jan 2021 00:00:00 GMT", "ID":"qH057","main_inca":1}
		post_data_helper.storeGasIncaInDB(gas_inca_json)

	def test_store_processed_data_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,"String_")

	def test_store_processed_data_valid(self):
		processed_measurement_json= {"CO": 1986.208,"CO_ug_m3": 1986.208,"H2S_ug_m3": 43.404,"H2S": 43.404,
						   "NO2": 19.78,"NO2_ug_m3": 19.78,"O3": 3.126,"O3_ug_m3": 3.126,"VOC":0,"CO2":1,
						   "SO2": 4.388,"SO2_ug_m3": 4.388,"PM10": 35.349,"PM25": 11.678,"UVA":1,"UVB":1,
						   "alt": 0.0,"lat": -12.0402780000002,"lon": -77.0436090000003,"PM1":1,
						   "timestamp_zone": "Fri, 01 Jan 2021 00:00:00 GMT", "ID":"qH057",
						   "pressure":10,"humidity":25,"I_temperature":25,"temperature":21,"spl":1,"UV":1}
		post_data_helper.storeProcessedDataInDB(processed_measurement_json)

	def test_store_valid_processed_data_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,"String_")

	def test_store_valid_processed_data_valid(self):
		processed_measurement_json= {"CO": 1986.208,"CO_ug_m3": 1986.208,"H2S_ug_m3": 43.404,"H2S": 43.404,
						   "NO2": 19.78,"NO2_ug_m3": 19.78,"O3": 3.126,"O3_ug_m3": 3.126, "VOC":0,"CO2":1,
						   "SO2": 4.388,"SO2_ug_m3": 4.388,"PM10": 35.349,"PM25": 11.678, "UVA":1,"UVB":1,
						   "alt": 0.0,"lat": -12.0402780000002,"lon": -77.0436090000003,"PM1":1,
						   "timestamp_zone": "Tue, 05 Jan 2021 05:00:00 GMT", "ID":"qH004",
						   "timestamp": "Fri, 01 Jan 2021 00:00:00 GMT",
						   "pressure":10,"humidity":25,"I_temperature":25,"temperature":21,"spl":1,"UV":1}
		post_data_helper.storeValidProcessedDataInDB(processed_measurement_json,"qH004")

	def test_valid_time_of_valid_processed_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed)
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,1)
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,1,1)
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,"a","minute","hora","json",23,"inca")
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,1,"minute","hora","json",23,"inca")
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,1,"minute","hora",{},23,0.0)
		self.assertRaises(TypeError,post_data_helper.validTimeOfValidProcessed,1,"minute","hora",{},"qH001","inca")


	def test_valid_time_of_valid_processed_valid(self):
		naive_time = datetime.time(0,0,0,410000)
		date = datetime.date(2021, 1, 1)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		last_time_turn_on = timezone.localize(naive_datetime)
		data_json= {"CO": 1986.208,"CO_ug_m3": 1986.208,"H2S_ug_m3": 43.404,"H2S": 43.404,
					"NO2": 19.78,"NO2_ug_m3": 19.78,"O3": 3.126,"O3_ug_m3": 3.126, "VOC":0,"CO2":1,
					"SO2": 4.388,"SO2_ug_m3": 4.388,"PM10": 35.349,"PM25": 11.678, "UVA":1,"UVB":1,
					"alt": 0.0,"lat": -12.0402780000002,"lon": -77.0436090000003,"PM1":1,"ID":"qH057",
					"timestamp_zone": "Fri, 01 Jan 2021 05:00:00 GMT",
					"timestamp": "Fri, 01 Jan 2021 00:00:00 GMT",
					"pressure":10,"humidity":25,"I_temperature":25,"temperature":21,"spl":1,"UV":1}
		inca_value = 0.0
		product_id = "qH057"
		post_data_helper.validTimeOfValidProcessed(10,"minute", last_time_turn_on,data_json,product_id,inca_value)
		post_data_helper.validTimeOfValidProcessed(10,"hour", last_time_turn_on,data_json,product_id,inca_value)



if __name__ == '__main__':
    unittest.main(verbosity=2)