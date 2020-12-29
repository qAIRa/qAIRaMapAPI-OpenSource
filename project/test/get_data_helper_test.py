import unittest
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import project.main.data.get_data_helper as get_data_helper

class TestGetDataHelper(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_query_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,None)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001","2020/01/01")

	#def test_query_air_quality_valid(self):
	#	initial_timestamp = "02-09-2020 00:00:00"
	#	last_timestamp = "02-09-2020 00:01:00"
	#	date_format = '%d-%m-%Y %H:%M:%S'
	#	self.assertAlmostEqual(get_data_helper.queryDBAirQuality('qH021',initial_timestamp,last_timestamp,date_format),[])
	#	self.assertAlmostEqual(get_data_helper.queryDBAirQuality('qH100',initial_timestamp,last_timestamp,date_format),None)

	def test_query_gas_average_measurement_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,True)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,None)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,"qH001",1,2)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,"qH001",1)
		self.assertRaises(ValueError,get_data_helper.queryDBGasAverageMeasurement,"qH001","H2O")

	def test_query_gas_average_measurement_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","CO"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","H2S"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","NO2"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","O3"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","PM25"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","PM10"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","SO2"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH100","CO"),None)

	def test_query_valid_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,True)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,None)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,"qH001")
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,1,"02-09-2010 00:01:00",'%d-%m-%Y %H:%M:%S')
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,"02-09-2010 00:01:00",1,'%d-%m-%Y %H:%M:%S')

	#def test_query_valid_air_quality_valid(self):
	#	initial_timestamp = "02-09-2010 00:00:00"
	#	last_timestamp = "02-09-2010 00:01:00"
	#	self.assertAlmostEqual(get_data_helper.queryDBGasInca(initial_timestamp,last_timestamp),[])

	def test_query_processed_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,True)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,None)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001","")
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001",1,"02-09-2010 00:01:00",'%d-%m-%Y %H:%M:%S')
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001","02-09-2010 00:01:00",1,'%d-%m-%Y %H:%M:%S')

	def test_query_processed_valid(self):
		initial_timestamp = "20-12-2010 00:00:00"
		last_timestamp = "21-12-2010 00:01:00"
		#self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH004",initial_timestamp,last_timestamp),[])
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH100",initial_timestamp,last_timestamp),None)


if __name__ == '__main__':
    unittest.main(verbosity=2)