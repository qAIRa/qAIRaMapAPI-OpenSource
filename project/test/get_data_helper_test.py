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

if __name__ == '__main__':
    unittest.main(verbosity=2)