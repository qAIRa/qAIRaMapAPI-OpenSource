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
	def test_query_qhawax_mode_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,True)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,-5.0)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,None)
		self.assertRaises(TypeError,get_data_helper.getQhawaxMode,"String_")

	def test_query_qhawax_mode_valid(self):
		self.assertAlmostEqual(get_data_helper.getQhawaxMode(1),'Stand By')
		self.assertAlmostEqual(get_data_helper.getQhawaxMode(100),None)

	def test_query_comercial_name_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getComercialName)
		self.assertRaises(TypeError,get_data_helper.getComercialName,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getComercialName,True)
		self.assertRaises(TypeError,get_data_helper.getComercialName,-5.0)
		self.assertRaises(TypeError,get_data_helper.getComercialName,None)
		self.assertRaises(TypeError,get_data_helper.getComercialName,"String_")

	def test_query_comercial_name_valid(self):
		self.assertAlmostEqual(get_data_helper.getComercialName(4),"Test Aguitas 2.0")
		self.assertAlmostEqual(get_data_helper.getComercialName(20),None)

	def test_query_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,None)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBAirQuality,"qH001","2020/01/01")

	def test_query_air_quality_valid(self):
		initial_timestamp = "02-09-2020 00:00:00"
		last_timestamp = "02-09-2020 00:01:00"
		date_format = '%d-%m-%Y %H:%M:%S'
		self.assertAlmostEqual(get_data_helper.queryDBAirQuality('qH001',initial_timestamp,last_timestamp,date_format),[])
		self.assertAlmostEqual(get_data_helper.queryDBAirQuality('qH100',initial_timestamp,last_timestamp,date_format),None)

	def test_query_time_qhawax_history_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,True)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,None)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,"qH001")

	def test_query_time_qhawax_history_valid(self):
		initial_timestamp = "09-09-2020 00:51:45.877701+00:00"
		last_timestamp = "22-09-2020 08:11:57.877701+00:00"
		date_format = '%d-%m-%Y %H:%M:%S.%f%z'
		last_time_turn_on = datetime.datetime.strptime("09-09-2020 00:51:45.877701+00:00",date_format)
		last_registration_time = datetime.datetime.strptime("22-09-2020 08:11:57.877701+00:00",date_format)
		values = {'last_time_on': last_time_turn_on, 'last_time_registration': last_registration_time} 
		print(values)
		self.assertAlmostEqual(get_data_helper.getTimeQhawaxHistory(51),values)

	def test_query_gas_average_measurement_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,True)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,None)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,"qH001",1,2)

	def test_query_gas_average_measurement_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","CO"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","H2S"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","NO2"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","O3"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","PM25"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","PM10"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH004","SO2"),[])
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH100","CO"),None)

	def test_query_valid_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,None)
		self.assertRaises(TypeError,get_data_helper.queryDBValidAirQuality,"qH001",1,2)

	def test_query_valid_air_quality_valid(self):
		initial_timestamp = "02-09-2020 00:00:00"
		last_timestamp = "02-09-2020 00:01:00"
		self.assertAlmostEqual(get_data_helper.queryDBValidAirQuality(1,initial_timestamp,last_timestamp),[])
		self.assertAlmostEqual(get_data_helper.queryDBValidAirQuality(100,initial_timestamp,last_timestamp),None)

	def test_query_valid_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,True)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,None)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBGasInca,1,"qH001")

	def test_query_valid_air_quality_valid(self):
		initial_timestamp = "02-09-2010 00:00:00"
		last_timestamp = "02-09-2010 00:01:00"
		date_format = '%d-%m-%Y %H:%M:%S'
		self.assertAlmostEqual(get_data_helper.queryDBGasInca(initial_timestamp,last_timestamp,date_format),[])

	def test_query_processed_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,True)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,None)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001",1)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001","",1)
		self.assertRaises(TypeError,get_data_helper.queryDBProcessed,"qH001",1,"")

	def test_query_processed_valid(self):
		initial_timestamp = "02-09-2010 00:00:00"
		last_timestamp = "02-09-2010 00:01:00"
		date_format = '%d-%m-%Y %H:%M:%S'
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH001",initial_timestamp,last_timestamp,date_format),[])
		self.assertAlmostEqual(get_data_helper.queryDBProcessed("qH100",initial_timestamp,last_timestamp,date_format),None)

	def test_query_noise_data_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getNoiseData)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getNoiseData,True)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,-5.0)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,None)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,"qH001",1,2)

	def test_query_noise_data_valid(self):
		self.assertAlmostEqual(get_data_helper.getNoiseData("qH004"),"Zona de Protección Especial")
		self.assertAlmostEqual(get_data_helper.getNoiseData("qH100"),None)

	def test_get_hours_difference_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getHoursDifference)
		self.assertRaises(TypeError,get_data_helper.getHoursDifference,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getHoursDifference,True)
		self.assertRaises(TypeError,get_data_helper.getHoursDifference,-5.0)
		self.assertRaises(TypeError,get_data_helper.getHoursDifference,None)
		self.assertRaises(TypeError,get_data_helper.getHoursDifference,"qH001",1,2)

	def test_get_hours_difference_valid(self):
		self.assertAlmostEqual(get_data_helper.getHoursDifference(100),(None,None))

	def test_get_valid_processed_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,True)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,None)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,1,2)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,2,"",5)
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,2,5,"")

	def test_get_valid_processed_valid(self):
		initial_timestamp = "02-09-2010 00:00:00"
		last_timestamp = "02-09-2010 00:01:00"
		date_format = '%d-%m-%Y %H:%M:%S'
		self.assertAlmostEqual(get_data_helper.queryDBValidProcessedByQhawaxScript(100,initial_timestamp,last_timestamp,date_format),None)
		self.assertAlmostEqual(get_data_helper.queryDBValidProcessedByQhawaxScript(4,initial_timestamp,last_timestamp,date_format),[])

	def test_get_latest_timestamp_valid_processed_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed)
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed,True)
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed,-5.0)
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed,None)
		self.assertRaises(TypeError,get_data_helper.getLatestTimestampValidProcessed,1)

	def test_get_latest_timestamp_valid_processed_valid(self):
		self.assertAlmostEqual(get_data_helper.getLatestTimestampValidProcessed("qH100"),None)

	def test_get_measurement_valid_processed_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,True)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,None)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,1)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,1,"",1)
		self.assertRaises(TypeError,get_data_helper.queryDBDailyValidProcessedByQhawaxScript,1,1,"")

	def test_get_measurement_valid_processed_valid(self):
		initial_timestamp = "02-09-2010 00:00:00"
		last_timestamp = "02-09-2010 00:01:00"
		date_format = '%d-%m-%Y %H:%M:%S'
		self.assertAlmostEqual(get_data_helper.queryDBDailyValidProcessedByQhawaxScript(100,initial_timestamp,last_timestamp,date_format),None)
		self.assertAlmostEqual(get_data_helper.queryDBDailyValidProcessedByQhawaxScript(4,initial_timestamp,last_timestamp,date_format),[])

	def test_get_query_db_air_quality_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality)
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality,True)
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality,4,"a",2020,40,2020)
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality,4,35,"a",40,2020)
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality,4,35,2020,"a",2020)
		self.assertRaises(TypeError,get_data_helper.queryDBAirDailyQuality,4,35,2020,40,"a")
		self.assertRaises(ValueError,get_data_helper.queryDBAirDailyQuality,4,45,2020,40,2020)
		self.assertRaises(ValueError,get_data_helper.queryDBAirDailyQuality,4,30,2020,40,2000)

	def test_get_query_db_air_quality_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBAirDailyQuality(100,30,2020,40,2020),None)
		self.assertAlmostEqual(get_data_helper.queryDBAirDailyQuality(4,1,2020,5,2020),[])

if __name__ == '__main__':
    unittest.main(verbosity=2)