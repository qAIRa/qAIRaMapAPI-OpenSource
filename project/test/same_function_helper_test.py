import unittest
import project.main.same_function_helper as same_helper

class TestSameFunctionHelper(unittest.TestCase):
	"""
	Test of Same Function Helper

	"""
	def test_qhawax_exist_based_on_id_not_valid(self):
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnID)
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnID,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnID,"4.33")
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnID,None)
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnID,True)

	def test_qhawax_exist_based_on_id_valid(self):
		self.assertAlmostEqual(same_helper.qhawaxExistBasedOnID(1),True)
		self.assertAlmostEqual(same_helper.qhawaxExistBasedOnID(100),False)

	def test_qhawax_exist_based_on_name_not_valid(self):
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnName)
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnName,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnName,4.55)
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnName,None)
		self.assertRaises(TypeError,same_helper.qhawaxExistBasedOnName,True)

	def test_qhawax_exist_based_on_name_valid(self):
		self.assertAlmostEqual(same_helper.qhawaxExistBasedOnName("qH001"),True)
		self.assertAlmostEqual(same_helper.qhawaxExistBasedOnName("qH100"),False)

	def test_qhawax_installation_exist_based_on_id_not_valid(self):
		self.assertRaises(TypeError,same_helper.qhawaxInstallationExistBasedOnID)
		self.assertRaises(TypeError,same_helper.qhawaxInstallationExistBasedOnID,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.qhawaxInstallationExistBasedOnID,"4.55")
		self.assertRaises(TypeError,same_helper.qhawaxInstallationExistBasedOnID,None)
		self.assertRaises(TypeError,same_helper.qhawaxInstallationExistBasedOnID,True)

	def test_qhawax_installation_exist_based_on_id_valid(self):
		self.assertAlmostEqual(same_helper.qhawaxInstallationExistBasedOnID(10),True)
		self.assertAlmostEqual(same_helper.qhawaxInstallationExistBasedOnID(51),True)
		self.assertAlmostEqual(same_helper.qhawaxInstallationExistBasedOnID(100),False)

	def test_area_exist_based_on_id_not_valid(self):
		self.assertRaises(TypeError,same_helper.areaExistBasedOnID)
		self.assertRaises(TypeError,same_helper.areaExistBasedOnID,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.areaExistBasedOnID,"4.55")
		self.assertRaises(TypeError,same_helper.areaExistBasedOnID,None)
		self.assertRaises(TypeError,same_helper.areaExistBasedOnID,True)

	def test_area_exist_based_on_id_valid(self):
		self.assertAlmostEqual(same_helper.areaExistBasedOnID(1),True)
		self.assertAlmostEqual(same_helper.areaExistBasedOnID(2),True)
		self.assertAlmostEqual(same_helper.areaExistBasedOnID(10),False)

	def test_company_exist_based_on_name_not_valid(self):
		self.assertRaises(TypeError,same_helper.companyExistBasedOnName)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnName,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.companyExistBasedOnName,4.55)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnName,None)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnName,True)

	def test_company_exist_based_on_name_valid(self):
		self.assertAlmostEqual(same_helper.companyExistBasedOnName("C40"),True)
		self.assertAlmostEqual(same_helper.companyExistBasedOnName("Huawei Test 20"),False)

	def test_company_exist_based_on_ruc_not_valid(self):
		self.assertRaises(TypeError,same_helper.companyExistBasedOnRUC)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnRUC,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.companyExistBasedOnRUC,4.55)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnRUC,None)
		self.assertRaises(TypeError,same_helper.companyExistBasedOnRUC,True)

	def test_company_exist_based_on_ruc_valid(self):
		self.assertAlmostEqual(same_helper.companyExistBasedOnRUC("10005678112"),True)
		self.assertAlmostEqual(same_helper.companyExistBasedOnRUC("12345678119"),False)

	def test_get_qhawax_id_not_valid(self):
		self.assertRaises(TypeError,same_helper.getQhawaxID)
		self.assertRaises(TypeError,same_helper.getQhawaxID,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.getQhawaxID,4.55)
		self.assertRaises(TypeError,same_helper.getQhawaxID,None)
		self.assertRaises(TypeError,same_helper.getQhawaxID,True)

	def test_get_qhawax_id_valid(self):
		self.assertAlmostEqual(same_helper.getQhawaxID("qH001"),1)
		self.assertAlmostEqual(same_helper.getQhawaxID("qH100"),None)

	def test_get_installation_not_valid(self):
		self.assertRaises(TypeError,same_helper.getInstallationId)
		self.assertRaises(TypeError,same_helper.getInstallationId,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.getInstallationId,"4.55")
		self.assertRaises(TypeError,same_helper.getInstallationId,None)
		self.assertRaises(TypeError,same_helper.getInstallationId,True)

	def test_get_installation_valid(self):
		self.assertAlmostEqual(same_helper.getInstallationId(4),51)
		self.assertAlmostEqual(same_helper.getInstallationId(100),None)

	def test_get_qhawax_name_not_valid(self):
		self.assertRaises(TypeError,same_helper.getQhawaxName)
		self.assertRaises(TypeError,same_helper.getQhawaxName,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.getQhawaxName,"4.55")
		self.assertRaises(TypeError,same_helper.getQhawaxName,None)
		self.assertRaises(TypeError,same_helper.getQhawaxName,True)

	def test_get_qhawax_name_valid(self):
		self.assertAlmostEqual(same_helper.getQhawaxName(1),"qH001")
		self.assertAlmostEqual(same_helper.getQhawaxName(100),None)

	def test_get_installation_id_based_name_not_valid(self):
		self.assertRaises(TypeError,same_helper.getInstallationIdBaseName)
		self.assertRaises(TypeError,same_helper.getInstallationIdBaseName,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.getInstallationIdBaseName,4.55)
		self.assertRaises(TypeError,same_helper.getInstallationIdBaseName,None)
		self.assertRaises(TypeError,same_helper.getInstallationIdBaseName,True)

	def test_get_installation_id_based_name_valid(self):
		self.assertAlmostEqual(same_helper.getInstallationIdBaseName("qH004"),51)
		self.assertAlmostEqual(same_helper.getInstallationIdBaseName("qH100"),None)

	def test_get_main_inca_not_valid(self):
		self.assertRaises(TypeError,same_helper.getMainIncaQhawaxTable)
		self.assertRaises(TypeError,same_helper.getMainIncaQhawaxTable,{"name":"qH001"})
		self.assertRaises(TypeError,same_helper.getMainIncaQhawaxTable,"4.55")
		self.assertRaises(TypeError,same_helper.getMainIncaQhawaxTable,None)
		self.assertRaises(TypeError,same_helper.getMainIncaQhawaxTable,True)

	def test_get_main_inca_valid(self):
		self.assertAlmostEqual(same_helper.getMainIncaQhawaxTable(4),-1)
		self.assertAlmostEqual(same_helper.getMainIncaQhawaxTable(100),None)


if __name__ == '__main__':
    unittest.main(verbosity=2)