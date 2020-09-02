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

	def test_get_average_not_valid(self):
		self.assertRaises(TypeError,util_helper.getAverage)
		self.assertRaises(TypeError,util_helper.getAverage,{"name":"qH001"})
		self.assertRaises(TypeError,util_helper.getAverage,"resultado")
		self.assertRaises(TypeError,util_helper.getAverage,-1)
		self.assertRaises(TypeError,util_helper.getAverage,None)
		self.assertRaises(TypeError,util_helper.getAverage,True)

if __name__ == '__main__':
    unittest.main(verbosity=2)