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


if __name__ == '__main__':
    unittest.main(verbosity=2)