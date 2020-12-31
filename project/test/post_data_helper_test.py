import unittest
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import project.main.data.post_data_helper as post_data_helper

class TestPostDataHelper(unittest.TestCase):
	""" Test of Post Data Functions """
	def test_store_air_quality_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,"String_")

	#def test_store_air_quality_valid(self):
	#	air_quality_json= {"CO": 1986.208,"CO_ug_m3": 1986.208,"H2S_ug_m3": 43.404,"H2S": 43.404,
	#					   "NO2": 19.78,"NO2_ug_m3": 19.78,"O3": 3.126,"O3_ug_m3": 3.126,
	#					   "SO2": 4.388,"SO2_ug_m3": 4.388,"PM10": 35.349,"PM25": 11.678,
	#					   "alt": 0.0,"lat": -12.0402780000002,"lon": -77.0436090000003,
	#					   "timestamp_zone": "Wed, 02 Sep 2020 00:00:00 GMT"}

	def test_store_gas_inca_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeGasIncaInDB,"String_")

	def test_store_processed_data_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeProcessedDataInDB,"String_")

	def test_store_valid_processed_data_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,"String_")


if __name__ == '__main__':
    unittest.main(verbosity=2)