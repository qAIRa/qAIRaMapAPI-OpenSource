import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper
from datetime import timedelta
import dateutil.parser
import unittest
import dateutil
import datetime
import pytz

class TestGetDataHelper(unittest.TestCase):
	""" Test of Get Data Functions """
	def test_query_air_valid_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,None)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,"qH001","2020/01/01")

	def test_query_air_valid_quality_valid(self):
		initial_timestamp = "02-09-2020 00:00:00"
		last_timestamp = "02-09-2020 05:01:00"
		self.assertAlmostEqual(get_data_helper.queryDBValidAirQuality(1,initial_timestamp,last_timestamp),[])
		self.assertAlmostEqual(get_data_helper.queryDBValidAirQuality(100,initial_timestamp,last_timestamp),None)

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
		naive_time = datetime.time(0,0,0)
		date = datetime.date(2021, 1, 6)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		aware_datetime = timezone.localize(naive_datetime)
		co = [(aware_datetime, 1986.208)]
		h2s = [(aware_datetime, 43.404)]
		no2 = [(aware_datetime, 19.78)]
		o3 = [(aware_datetime, 3.126)]
		so2 = [(aware_datetime, 4.388)]
		pm25 = [(aware_datetime, 11.678)]
		pm10 = [(aware_datetime, 35.349)]
		co_format = [{'timestamp_zone': aware_datetime, 'sensor': 1986.208}]
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","CO"),co)
		self.assertAlmostEqual(util_helper.getFormatData(get_data_helper.queryDBGasAverageMeasurement("qH057","CO")),co_format)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","H2S"),h2s)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","NO2"),no2)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","O3"),o3)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","PM25"),pm25)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","PM10"),pm10)
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH057","SO2"),so2)
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

	def test_query_valid_air_quality_valid(self):
		initial_timestamp = "02-09-2010 00:00:00"
		last_timestamp = "02-09-2010 00:01:00"
		self.assertAlmostEqual(get_data_helper.queryDBGasInca(initial_timestamp,last_timestamp),[])

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
		naive_time = datetime.time(5,0,21)
		date = datetime.date(2020, 12, 20)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		initial_timestamp = timezone.localize(naive_datetime)
		date = datetime.date(2020, 12, 21)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		last_timestamp = timezone.localize(naive_datetime)
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH004",initial_timestamp,last_timestamp),[])
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH100",initial_timestamp,last_timestamp),None)

	def test_query_last_main_inca_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,True)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,None)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,1)

	def test_query_last_main_inca_valid(self):
		self.assertAlmostEqual(get_data_helper.queryLastMainInca("qH004"),500.0)
		self.assertAlmostEqual(get_data_helper.queryLastMainInca("qH100"),None)

	def test_query_first_timestamp_valid_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,True)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,-5.0)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,None)

	def test_query_first_timestamp_valid_valid(self):
		naive_time = datetime.time(5,0,21)
		date = datetime.date(2020, 12, 31)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		aware_datetime = timezone.localize(naive_datetime)
		self.assertAlmostEqual(get_data_helper.getFirstTimestampValidProcessed(1),aware_datetime)
		self.assertAlmostEqual(get_data_helper.getFirstTimestampValidProcessed(100),None)


if __name__ == '__main__':
    unittest.main(verbosity=2)