import unittest
import datetime
from datetime import timedelta
import project.main.exceptions as exception_helper

class TestMainExceptions(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_query_company_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,True)

	def test_query_offset_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson)
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getOffsetTargetofJson,True)

	def test_query_controlled_offset_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson)
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getControlledOffsetTargetofJson,True)

	def test_query_non_controlled_offset_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson)
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getNonControlledOffsetTargetofJson,True)

	def test_query_qhawax_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,True)

	def test_query_inca_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,True)

	def test_query_off_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,True)

	def test_query_on_target_json_not_valid(self):
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,True)

if __name__ == '__main__':
    unittest.main(verbosity=2)