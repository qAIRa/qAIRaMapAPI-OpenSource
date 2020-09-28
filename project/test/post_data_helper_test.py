import unittest
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import project.main.data.post_data_helper as post_data_helper

class TestPostDataHelper(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_store_air_quality_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeAirQualityDataInDB,"String_")

	#def test_store_air_quality_valid(self):
	#	air_quality_json= {}

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
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,True,1)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeValidProcessedDataInDB,"String_")

	def test_store_air_daily_quality_data_not_valid(self):
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB)
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB,True,1)
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB,True)
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB,-5.0)
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB,None)
		self.assertRaises(TypeError,post_data_helper.storeAirDailyQualityDataInDB,"String_")

if __name__ == '__main__':
    unittest.main(verbosity=2)