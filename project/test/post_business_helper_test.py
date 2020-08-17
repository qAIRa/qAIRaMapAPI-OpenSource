import unittest

import project.main.business.post_business_helper as post_business_helper

class TestPostBusinessData(unittest.TestCase):
	"""
	Test of Post Business Functions

	"""

	def test_create_company_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.createCompany)
		self.assertRaises(TypeError,post_business_helper.createCompany,4,None)
		self.assertRaises(TypeError,post_business_helper.createCompany,None,4)
		self.assertRaises(TypeError,post_business_helper.createCompany,"PUCP",None)
		self.assertRaises(TypeError,post_business_helper.createCompany,None,"pucp.edu.pe")

	def test_write_binnacle_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.writeBinnacle)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,None,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,4,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004",4,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004",None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,80)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,80,None,None,None)

	def test_update_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,80)

	def test_update_controlled_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,80)

	def test_update_non_controlled_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,80)

if __name__ == '__main__':
    unittest.main(verbosity=2)
