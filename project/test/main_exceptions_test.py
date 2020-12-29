import unittest
import datetime
from datetime import timedelta
import project.main.exceptions as exception_helper

class TestMainExceptions(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_query_company_target_json_not_valid(self):
		data = {'company_name':'test','email_group':'test.test','ruc':1001}
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,5)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getCompanyTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getCompanyTargetofJson,data)

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

	def test_query_qhawax_target_json_valid(self):
		data = {'qhawax_name':'test','description':'test','person_in_charge':'test', 'qhawax_type':'test'}
		self.assertAlmostEqual(exception_helper.getQhawaxTargetofJson(data),(str(data['qhawax_name']),\
																			str(data['qhawax_type']),\
																			str(data['person_in_charge']),\
																			str(data['description'])))
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

	def test_query_inca_target_json_valid(self):
		data = {'name':'test','value_inca':100}
		self.assertAlmostEqual(exception_helper.getIncaTargetofJson(data),(str(data['name']).strip(),data['value_inca']))

	def test_query_off_target_json_not_valid(self):
		data_qhawax_name= {'qhawax_lost_timestamp':'test'}
		data_qhawax_lost_time= {'qhawax_name':'test'}
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,"Json")
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,4.33)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,None)
		self.assertRaises(TypeError,exception_helper.getStatusOffTargetofJson,True)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getStatusOffTargetofJson,data_qhawax_lost_time)

	def test_query_off_target_json_valid(self):
		data = {'qhawax_name':'test','qhawax_lost_timestamp':'test'}
		self.assertAlmostEqual(exception_helper.getStatusOffTargetofJson(data),(str(data['qhawax_name']).strip(),\
																		   	   data['qhawax_lost_timestamp']))

	def test_query_change_to_calibration_json_not_valid(self):
		data_qhawax_name= {'person_in_charge':'test'}
		data_person_in_charge= {'qhawax_name':'test'}
		self.assertRaises(TypeError,exception_helper.getChangeCalibrationFields)
		self.assertRaises(TypeError,exception_helper.getChangeCalibrationFields,"Json")
		self.assertRaises(TypeError,exception_helper.getChangeCalibrationFields,4.33)
		self.assertRaises(TypeError,exception_helper.getChangeCalibrationFields,None)
		self.assertRaises(TypeError,exception_helper.getChangeCalibrationFields,True)
		self.assertRaises(ValueError,exception_helper.getChangeCalibrationFields,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getChangeCalibrationFields,data_person_in_charge)

	def test_query_change_to_calibration_json_valid(self):
		data = {'qhawax_name':'test','person_in_charge':'test'}
		self.assertAlmostEqual(exception_helper.getChangeCalibrationFields(data),(str(data['qhawax_name']).strip(),\
																				 data['person_in_charge']))

	def test_query_end_calibration_json_not_valid(self):
		data_qhawax_name= {'person_in_charge':'test'}
		data_person_in_charge = {'qhawax_name':'test'}
		self.assertRaises(TypeError,exception_helper.getEndCalibrationFields)
		self.assertRaises(TypeError,exception_helper.getEndCalibrationFields,"Json")
		self.assertRaises(TypeError,exception_helper.getEndCalibrationFields,4.33)
		self.assertRaises(TypeError,exception_helper.getEndCalibrationFields,None)
		self.assertRaises(TypeError,exception_helper.getEndCalibrationFields,True)
		self.assertRaises(ValueError,exception_helper.getEndCalibrationFields,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getEndCalibrationFields,data_person_in_charge)

	def test_query_end_calibration_json_valid(self):
		data = {'qhawax_name':'test','person_in_charge':'test'}
		self.assertAlmostEqual(exception_helper.getEndCalibrationFields(data),(str(data['qhawax_name']).strip(),\
																			  str(data['person_in_charge'])))

	def test_query_installation_fields_json_not_valid(self):
		data_qhawax_name= {'person_in_charge':'test'}
		data_person_in_charge= {'qhawax_name':'test'}
		self.assertRaises(TypeError,exception_helper.getInstallationFields)
		self.assertRaises(TypeError,exception_helper.getInstallationFields,"Json")
		self.assertRaises(TypeError,exception_helper.getInstallationFields,4.33)
		self.assertRaises(TypeError,exception_helper.getInstallationFields,None)
		self.assertRaises(TypeError,exception_helper.getInstallationFields,True)
		self.assertRaises(ValueError,exception_helper.getInstallationFields,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getInstallationFields,data_person_in_charge)

	def test_query_installation_fields_json_valid(self):
		data = {'qhawax_name':'test','person_in_charge':'test'}
		self.assertAlmostEqual(exception_helper.getInstallationFields(data),(str(data['qhawax_name']),\
																			str(data['person_in_charge'])))

	def test_query_end_work_fields_json_not_valid(self):
		data_qhawax_name= {'person_in_charge':'test','end_date':'test'}
		data_person_in_charge= {'qhawax_name':'test','end_date':'test'}
		data_end_date= {'qhawax_name':'test','person_in_charge':'test'}
		self.assertRaises(TypeError,exception_helper.validEndWorkFieldJson)
		self.assertRaises(TypeError,exception_helper.validEndWorkFieldJson,"Json")
		self.assertRaises(TypeError,exception_helper.validEndWorkFieldJson,4.33)
		self.assertRaises(TypeError,exception_helper.validEndWorkFieldJson,None)
		self.assertRaises(TypeError,exception_helper.validEndWorkFieldJson,True)
		self.assertRaises(ValueError,exception_helper.validEndWorkFieldJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.validEndWorkFieldJson,data_person_in_charge)
		self.assertRaises(ValueError,exception_helper.validEndWorkFieldJson,data_end_date)

	def test_query_end_work_fields_json_not_valid(self):
		data = {'qhawax_name':'test','person_in_charge':'test','end_date':'test'}
		self.assertAlmostEqual(exception_helper.validEndWorkFieldJson(data),(str(data['qhawax_name']),\
																			data['end_date'],\
																			str(data['person_in_charge'])))

	def test_query_end_calibration_json_not_valid(self):
		data_qhawax_name= {'timestamp_turn_on_conection':'test'}
		data_timestamp_turn_on_conection = {'qhawax_name':'test'}
		self.assertRaises(TypeError,exception_helper.getQhawaxSignalJson)
		self.assertRaises(TypeError,exception_helper.getQhawaxSignalJson,"Json")
		self.assertRaises(TypeError,exception_helper.getQhawaxSignalJson,4.33)
		self.assertRaises(TypeError,exception_helper.getQhawaxSignalJson,None)
		self.assertRaises(TypeError,exception_helper.getQhawaxSignalJson,True)
		self.assertRaises(ValueError,exception_helper.getQhawaxSignalJson,data_qhawax_name)
		self.assertRaises(ValueError,exception_helper.getQhawaxSignalJson,data_timestamp_turn_on_conection)

	def test_query_end_calibration_json_valid(self):
		data = {'qhawax_name':'test','timestamp_turn_on_conection':'test'}
		self.assertAlmostEqual(exception_helper.getQhawaxSignalJson(data),(str(data['qhawax_name']).strip(),\
																		   str(data['timestamp_turn_on_conection'])))

if __name__ == '__main__':
    unittest.main(verbosity=2)