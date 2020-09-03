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

	#def test_get_gas_sensor_json_valid(self):
	#	json = {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}
	#	sensors = [('NO', 0.0, 0.0, 0.0, 0.0), ('CO', 0.0, 0.0, 0.0, 0.0), ('O3', 0.0, 0.0, 0.0, 0.0),
	#			   ('H2S', 0.0, 0.0, 0.0, 0.0), ('NO2', 0.0, 0.0, 0.0, 0.0), ('SO2', 0.0, 0.0, 0.0, 0.0)]
	#	json_output = {'CO': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
	#				   'SO2': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
	#				   'H2S': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
	#				   'O3': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0},
	#				   'NO': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0},
	#				   'NO2': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}}
	#	self.assertAlmostEqual(util_helper.gasSensorJson(json,sensors),json_output)

	#def test_get_color_based_inca_not_valid(self):
	#	self.assertRaises(TypeError,util_helper.getColorBaseOnIncaValue)
	#	self.assertRaises(TypeError,util_helper.getColorBaseOnIncaValue,{"name":"qH001"})
	#	self.assertRaises(TypeError,util_helper.getColorBaseOnIncaValue,"resultado")
	#	self.assertRaises(TypeError,util_helper.getColorBaseOnIncaValue,None)
	#	self.assertRaises(TypeError,util_helper.getColorBaseOnIncaValue,True)

	#def test_get_color_based_inca_not_valid(self):
	#	self.assertAlmostEqual(util_helper.getColorBaseOnIncaValue(int(50.0)),'green')
	#	self.assertAlmostEqual(util_helper.getColorBaseOnIncaValue(int(100.0)),'yellow')

if __name__ == '__main__':
    unittest.main(verbosity=2)