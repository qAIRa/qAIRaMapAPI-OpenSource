
import project.main.exceptions as exceptions

class TestException(unittest.TestCase):
	"""
	Test of Get Business Functions

	"""
	def test_company_target_not_valid(self):
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		company_1 ={"company_name":"","email_group":"","ruc":"","address":"","phone":"","contact_person":""}
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson)
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson,"json")
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson,4.33)
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson,5)
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson,None)
		self.assertRaises(TypeError,exceptions.getCompanyTargetofJson,True)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)
		self.assertRaises(ValueError,exceptions.getCompanyTargetofJson,company_1)

