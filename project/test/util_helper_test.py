import unittest
import datetime
from datetime import timedelta
import project.main.util_helper as util_helper

class TestUtilHelper(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_check_date_not_valid(self):
		self.assertRaises(TypeError,util_helper.check_valid_date,{"name":"qH001"})
		self.assertRaises(TypeError,util_helper.check_valid_date,4.33)
		self.assertRaises(TypeError,util_helper.check_valid_date,5)
		self.assertRaises(TypeError,util_helper.check_valid_date,None)
		self.assertRaises(TypeError,util_helper.check_valid_date,True)

	def test_check_time_not_valid(self):
		self.assertRaises(TypeError,util_helper.getValidTime)
		self.assertRaises(TypeError,util_helper.getValidTime,{"name":"qH001"})
		self.assertRaises(TypeError,util_helper.getValidTime,4.33)
		self.assertRaises(TypeError,util_helper.getValidTime,5)
		self.assertRaises(TypeError,util_helper.getValidTime,None)
		self.assertRaises(TypeError,util_helper.getValidTime,True)

	def test_get_gas_sensor_json_not_valid(self):
		self.assertRaises(TypeError,util_helper.gasSensorJson)
		self.assertRaises(TypeError,util_helper.gasSensorJson,{"name":"qH001"})
		self.assertRaises(TypeError,util_helper.gasSensorJson,"resultado")
		self.assertRaises(TypeError,util_helper.gasSensorJson,None)
		self.assertRaises(TypeError,util_helper.gasSensorJson,True)

	def test_are_fields_correct_not_valid(self):
		self.assertRaises(TypeError,util_helper.areFieldsValid)
		self.assertRaises(TypeError,util_helper.areFieldsValid,5)
		self.assertRaises(TypeError,util_helper.areFieldsValid,"resultado")
		self.assertRaises(TypeError,util_helper.areFieldsValid,None)
		self.assertRaises(TypeError,util_helper.areFieldsValid,True)

	def test_check_negatives_not_valid(self):
		self.assertRaises(TypeError,util_helper.checkNegatives)
		self.assertRaises(TypeError,util_helper.checkNegatives,5)
		self.assertRaises(TypeError,util_helper.checkNegatives,"resultado")
		self.assertRaises(TypeError,util_helper.checkNegatives,None)
		self.assertRaises(TypeError,util_helper.checkNegatives,True)

	def test_check_number_values_not_valid(self):
		self.assertRaises(TypeError,util_helper.checkNumberValues)
		self.assertRaises(TypeError,util_helper.checkNumberValues,5)
		self.assertRaises(TypeError,util_helper.checkNumberValues,"resultado")
		self.assertRaises(TypeError,util_helper.checkNumberValues,None)
		self.assertRaises(TypeError,util_helper.checkNumberValues,True)

	def test_check_number_values_valid(self):
		y = {'ID': 'qH004', 'timestamp': '2020-08-31 00:00:00.0-05:00', 'lat': -12.072736, 
			 'lon': -77.082687, 'CO': 162.379, 'H2S': 0, 'NO2': 1.218, 'O3': 0, 'SO2': 0.77, 
			 'PM1': 0, 'PM25': 0, 'PM10': 0, 'UV': 'Nan', 'UVA': 'Nan', 'UVB': 'Nan', 'spl': 0,
			 'temperature': 19.1, 'pressure': 100743.24, 'humidity': 71.9}
		self.assertAlmostEqual(util_helper.checkNumberValues(y),y)

	def test_round_up_three_not_valid(self):
		self.assertRaises(TypeError,util_helper.roundUpThree)
		self.assertRaises(TypeError,util_helper.roundUpThree,5)
		self.assertRaises(TypeError,util_helper.roundUpThree,"resultado")
		self.assertRaises(TypeError,util_helper.roundUpThree,None)
		self.assertRaises(TypeError,util_helper.roundUpThree,True)

	def test_round_up_three_valid(self):
		y = {'ID': 'qH004', 'CO': 162.379, 'CO_ug_m3': 186.73584999999997, 'H2S': 0, 'H2S_ug_m3': 0.0,
			 'NO2': 1.218, 'NO2_ug_m3': 2.28984, 'O3': 0, 'O3_ug_m3': 0.0, 'PM1': 0, 'PM10': 0, 'PM25': 0,
			 'SO2': 0.77, 'SO2_ug_m3': 2.0174000000000003, 'spl': 0, 'UV': 0, 'UVA': 0, 'UVB': 0, 
			 'humidity': 71.9, 'lat': -12.072736, 'lon': -77.082687, 'pressure': 100743.24, 'temperature': 19.1,
			 'timestamp': '2020-08-31 00:00:00.0-05:00'}
		last_y = {'ID': 'qH004', 'CO': 162.379, 'CO_ug_m3': 186.736, 'H2S': 0,'H2S_ug_m3': 0.0, 'NO2': 1.218,'NO2_ug_m3': 2.29, 'O3': 0, 'O3_ug_m3': 0.0, 'PM1': 0, 'PM10': 0, 'PM25': 0, 'SO2': 0.77, 'SO2_ug_m3': 2.017, 'spl': 0, 'UV': 0, 'UVA': 0, 'UVB': 0, 'humidity': 71.9, 'lat': -12.072736,'lon': -77.082687, 'pressure': 100743.24, 'temperature': 19.1,'timestamp': '2020-08-31 00:00:00.0-05:00'}
		self.assertAlmostEqual(util_helper.roundUpThree(y),last_y)

	def test_average_measurements_not_valid(self):
		self.assertRaises(TypeError,util_helper.averageMeasurements)
		self.assertRaises(TypeError,util_helper.averageMeasurements,5)
		self.assertRaises(TypeError,util_helper.averageMeasurements,"resultado")
		self.assertRaises(TypeError,util_helper.averageMeasurements,None)
		self.assertRaises(TypeError,util_helper.averageMeasurements,True)



if __name__ == '__main__':
    unittest.main(verbosity=2)