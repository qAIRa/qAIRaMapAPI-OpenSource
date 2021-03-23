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
		qhawax = "qH057"
		naive_time1 = datetime.time(0,0,0)
		naive_time2 = datetime.time(1,0,0)
		naive_time3 = datetime.time(2,0,0)
		naive_time4 = datetime.time(4,0,0)
		date = datetime.date(2021, 1, 6)
		naive_datetime1 = datetime.datetime.combine(date, naive_time1)
		naive_datetime2 = datetime.datetime.combine(date, naive_time2)
		naive_datetime3 = datetime.datetime.combine(date, naive_time3)
		naive_datetime4 = datetime.datetime.combine(date, naive_time4)
		timezone = pytz.timezone('UTC')
		aware_datetime1 = timezone.localize(naive_datetime1)
		aware_datetime2 = timezone.localize(naive_datetime2)
		aware_datetime3 = timezone.localize(naive_datetime3)
		aware_datetime4 = timezone.localize(naive_datetime4)
		co = [(aware_datetime1, 1986.208),(aware_datetime4, 1986.208)]
		h2s = [(aware_datetime1, 43.404),(aware_datetime4, 43.404)]
		no2 = [(aware_datetime1, 19.78),(aware_datetime4, 19.78)]
		o3 = [(aware_datetime1, 3.126),(aware_datetime4, 3.126)]
		so2 = [(aware_datetime1, 4.388),(aware_datetime4, 4.388)]
		pm25 = [(aware_datetime1, 11.678),(aware_datetime4, 11.678)]
		pm10 = [(aware_datetime1, 35.349),(aware_datetime4, 35.349)]
		co_format = [{'timestamp_zone': aware_datetime1, 'sensor': 1986.208},{'timestamp_zone': aware_datetime2, 'sensor': ""},\
					 {'timestamp_zone': aware_datetime3, 'sensor': ""},{'timestamp_zone': aware_datetime4, 'sensor': 1986.208}]
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"CO"))
		#print(util_helper.getFormatData(get_data_helper.queryDBGasAverageMeasurement(qhawax,"CO")))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"H2S"))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"NO2"))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"O3"))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM25"))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM10"))
		#print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"SO2"))

		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"CO"),[])
		self.assertAlmostEqual(util_helper.getFormatData(get_data_helper.queryDBGasAverageMeasurement("qH057","CO")),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"H2S"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"NO2"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"O3"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM25"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM10"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement(qhawax,"SO2"),[])
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
		print(get_data_helper.queryDBProcessed("qH057",initial_timestamp,last_timestamp))
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH057",initial_timestamp,last_timestamp),[])
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH100",initial_timestamp,last_timestamp),None)

	def test_query_last_main_inca_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,True)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,None)
		self.assertRaises(TypeError,get_data_helper.queryLastMainInca,1)

	def test_query_last_main_inca_valid(self):
		self.assertAlmostEqual(get_data_helper.queryLastMainInca("qH004"),50.0)
		self.assertAlmostEqual(get_data_helper.queryLastMainInca("qH100"),None)

	def test_query_first_timestamp_valid_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,True)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,-5.0)
		self.assertRaises(TypeError,get_data_helper.getFirstTimestampValidProcessed,None)

	def test_query_first_timestamp_valid_valid(self):
		naive_time = datetime.time(21,14,2)
		date = datetime.date(2021, 3, 22)
		naive_datetime = datetime.datetime.combine(date, naive_time)
		timezone = pytz.timezone('UTC')
		aware_datetime = timezone.localize(naive_datetime)
		print(get_data_helper.getFirstTimestampValidProcessed(307))
		self.assertAlmostEqual(get_data_helper.getFirstTimestampValidProcessed(307),aware_datetime)
		self.assertAlmostEqual(get_data_helper.getFirstTimestampValidProcessed(100),None)


if __name__ == '__main__':
    unittest.main(verbosity=2)