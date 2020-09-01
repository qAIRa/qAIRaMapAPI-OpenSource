import unittest
import datetime
from datetime import timedelta
import project.main.data.get_data_helper as get_data_helper

class TestGetDataHelper(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_query_qhawax_mode_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,True)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,-5.0)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,None)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,"String_")

	def test_query_comercial_name_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getComercialName)
		self.assertRaises(TypeError,get_data_helper.getComercialName,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getComercialName,True)
		self.assertRaises(TypeError,get_data_helper.getComercialName,-5.0)
		self.assertRaises(TypeError,get_data_helper.getComercialName,None)
		self.assertRaises(TypeError,get_data_helper.getComercialName,"String_")

	def test_query_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,None)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001","2020/01/01")

	def test_query_time_qhawax_history_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,True)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,-5.0)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,None)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,"qH001",1,2)

	def test_query_noise_data_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getNoiseData)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getNoiseData,True)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,-5.0)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,None)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,"qH001",1,2)

if __name__ == '__main__':
    unittest.main(verbosity=2)