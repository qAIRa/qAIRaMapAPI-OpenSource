import unittest
import datetime
from datetime import timedelta
import project.main.exceptions as exception_helper

class TestMainExceptions(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_query_company_target_json_not_valid(self):
		data = {'company_name':'test','email_group':'test.test','ruc':1001,'address':'test'}
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getCompanyTargetofJson,data)

	def test_query_gas_sensor_target_json_not_valid(self):
		data_product_id = {'description':'test','person_in_charge':'test','gas_sensor_json':{}}
		data_description = {'product_id':1,'person_in_charge':'test','gas_sensor_json':{}}
		data_person_in_charge = {'product_id':1,'description':'test','gas_sensor_json':{}}
		data_gas_sensor = {'product_id':1,'description':'test','person_in_charge':'test'}
		self.assertRaises(TypeError,exception_helper.getGasSensorTargetofJson)
		self.assertRaises(TypeError,exception_helper.getGasSensorTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getGasSensorTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getGasSensorTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getGasSensorTargetofJson,data_product_id)
		self.assertRaises(ValueError,exception_helper.getGasSensorTargetofJson,data_description)
		self.assertRaises(ValueError,exception_helper.getGasSensorTargetofJson,data_person_in_charge)
		self.assertRaises(ValueError,exception_helper.getGasSensorTargetofJson,data_gas_sensor)

	def test_query_qhawax_target_json_not_valid(self):
		data_qhawax_name= {'qhawax_type':'test','person_in_charge':'test','description':'test'}
		data_qhawax_type = {'qhawax_name':'test','person_in_charge':'test','description':'test'}
		data_person_in_charge = {'qhawax_name':'test','qhawax_type':'test','description':'test'}
		data_description = {'qhawax_name':'test','qhawax_type':'test','person_in_charge':'test'}
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getQhawaxTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getQhawaxTargetofJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getQhawaxTargetofJson,data_qhawax_type)
		self.assertRaises(ValueError,exception_helper.getQhawaxTargetofJson,data_person_in_charge)
		self.assertRaises(ValueError,exception_helper.getQhawaxTargetofJson,data_description)

	def test_query_inca_target_json_not_valid(self):
		data_qhawax_name= {'value_inca':'test'}
		data_value_inca= {'name':'test'}
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getIncaTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getIncaTargetofJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getIncaTargetofJson,data_value_inca)

	def test_query_off_target_json_not_valid(self):
		data_qhawax_name= {'qhawax_lost_timestamp':'test','person_in_charge':'test','description':'test'}
		data_qhawax_lost_time= {'qhawax_name':'test','person_in_charge':'test','description':'test'}
		data_person_in_charge = {'qhawax_name':'test','qhawax_lost_timestamp':'test','description':'test'}
		data_description = {'qhawax_name':'test','qhawax_lost_timestamp':'test','person_in_charge':'test'}
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_qhawax_lost_time)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_person_in_charge)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_description)

	def test_query_on_target_json_not_valid(self):
		data_qhawax_name= {'person_in_charge':'test','description':'test'}
		data_person_in_charge= {'qhawax_name':'test','description':'test'}
		data_description = {'qhawax_name':'test','person_in_charge':'test'}
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getStatusOnTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getStatusOnTargetofJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getStatusOnTargetofJson,data_person_in_charge)
		self.assertRaises(ValueError,exception_helper.getStatusOnTargetofJson,data_description)

if __name__ == '__main__':
    unittest.main(verbosity=2)