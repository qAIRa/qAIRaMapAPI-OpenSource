import unittest

import project.main.business.post_business_helper as post_business_helper

class TestPostBusinessData(unittest.TestCase):
	"""
	Test of Post Business Functions

	"""

	def test_create_company_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.createCompany,4,None)
		self.assertRaises(TypeError,post_business_helper.createCompany,None,4)
		self.assertRaises(TypeError,post_business_helper.createCompany,"PUCP",None)
		self.assertRaises(TypeError,post_business_helper.createCompany,None,"pucp.edu.pe")



if __name__ == '__main__':
    unittest.main(verbosity=2)
