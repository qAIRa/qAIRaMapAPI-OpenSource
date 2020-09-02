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
		self.assertAlmostEqual(get_data_helper.queryDBAirQuality('qH100',"",""),None)

	def test_query_time_qhawax_history_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,True)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,-5.0)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,None)
		self.assertRaises(TypeError,get_data_helper.getTimeQhawaxHistory,"qH001",1,2)

	def test_query_time_qhawax_history_valid(self):
		self.assertAlmostEqual(get_data_helper.getTimeQhawaxHistory(100),None)

	def test_query_gas_average_measurement_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,True)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,-5.0)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,None)
		self.assertRaises(TypeError,get_data_helper.queryDBGasAverageMeasurement,"qH001",1,2)

	def test_query_gas_average_measurement_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBGasAverageMeasurement("qH100","CO",[]),None)

	def test_query_noise_data_not_valid(self):
		self.assertRaises(TypeError,get_data_helper.getNoiseData)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,{"qhawax_id":5})
		self.assertRaises(TypeError,get_data_helper.getNoiseData,True)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,-5.0)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,None)
		self.assertRaises(TypeError,get_data_helper.getNoiseData,"qH001",1,2)

	def test_query_noise_data_valid(self):
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
		self.assertRaises(TypeError,get_data_helper.queryDBValidProcessedByQhawaxScript,2)

	def test_get_valid_processed_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBValidProcessedByQhawaxScript(100,"",""),None)

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

	def test_get_measurement_valid_processed_valid(self):
		self.assertAlmostEqual(get_data_helper.queryDBDailyValidProcessedByQhawaxScript(100,"",""),None)

if __name__ == '__main__':
    unittest.main(verbosity=2)