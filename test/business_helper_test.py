import unittest

import project.main.business.business_helper as helper

class TestBusinessData(unittest.TestCase):
	"""
	Test Business Data Class

	"""
	def test_query_get_companies(self):
		companies = helper.queryGetCompanies()
		self.assertAlmostEqual(helper.queryGetCompanies(),companies)

	def test_create_company_not_valid(self):
		self.assertRaises(TypeError,helper.createCompany,4,None)
		self.assertRaises(TypeError,helper.createCompany,None,4)
		self.assertRaises(TypeError,helper.createCompany,"PUCP",None)
		self.assertRaises(TypeError,helper.createCompany,None,"pucp.edu.pe")

	def test_query_get_eca_noise(self):
		e1 = (1, 'Zona de Protección Especial', 50, 40)
		e2 = (2, 'Zona Residencial', 60, 50)
		self.assertAlmostEqual(helper.queryGetEcaNoise(1),e1)
		self.assertAlmostEqual(helper.queryGetEcaNoise(2),e2)

	def test_query_get_eca_noise_not_valid(self):
		self.assertRaises(TypeError,helper.queryGetEcaNoise,None)
		self.assertRaises(TypeError,helper.queryGetEcaNoise,4.33)
		self.assertRaises(TypeError,helper.queryGetEcaNoise,"PUCP")

	def test_query_get_areas(self):
		area_list = [(4, 'Zona Industrial'),(3, 'Zona Comercial'),(2, 'Zona Residencial'), (1, 'Zona de Protección Especial')]
		self.assertAlmostEqual(helper.queryGetAreas(),area_list)

	def test_query_get_offsets_from_productID(self):
		qhawax_name= 'qH001'
		offset_sensor ={'CO': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
					   'SO2': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
		               'H2S': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
		                'O3': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
		                'NO': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}, 
		               'NO2': {'WE': 0.0, 'AE': 0.0, 'sensitivity': 0.0, 'sensitivity_2': 0.0}}
		self.assertAlmostEqual(helper.getOffsetsFromProductID(qhawax_name),offset_sensor)

	def test_query_get_offsets_from_productID_not_valid(self):
		self.assertRaises(TypeError,helper.getOffsetsFromProductID,4)
		self.assertRaises(TypeError,helper.getOffsetsFromProductID,None)
		self.assertRaises(TypeError,helper.getOffsetsFromProductID,"342")

	def test_query_get_controlled_offsets_from_productID(self):
		qhawax_name= 'qH004'
		offset_sensor ={'CO': {'C2': 0.0, 'C1': 0.0, 'C0': 1.0}, 
		                'SO2': {'C2': 0.0, 'C1': 0.0, 'C0': 0.0}, 
		                'H2S': {'C2': 0.0, 'C1': 0.0, 'C0': 2.0}, 
		                'O3': {'C2': 0.0, 'C1': 0.0, 'C0': 0.0}, 
		                'NO': {'C2': 0.0, 'C1': 0.0, 'C0': 4.0}, 
		                'NO2': {'C2': 0.0, 'C1': 0.0, 'C0': 4.0}}
		print(helper.getControlledOffsetsFromProductID(qhawax_name))
		self.assertAlmostEqual(helper.getControlledOffsetsFromProductID(qhawax_name),offset_sensor)

	def test_query_get_controlled_offsets_from_productID_not_valid(self):
		self.assertRaises(TypeError,helper.getControlledOffsetsFromProductID,4)
		self.assertRaises(TypeError,helper.getControlledOffsetsFromProductID,None)
		self.assertRaises(TypeError,helper.getControlledOffsetsFromProductID,"342")

	def test_query_get_non_controlled_offsets_from_productID(self):
		qhawax_name= 'qH001'
		offset_sensor ={'CO': {'NC1': 0.0, 'NC0': 0.0}, 
		               'SO2': {'NC1': 0.0, 'NC0': 1.0}, 
		               'H2S': {'NC1': 0.0, 'NC0': 0.0}, 
		                'O3': {'NC1': 0.0, 'NC0': 0.0}, 
		                'NO': {'NC1': 0.0, 'NC0': 0.0}, 
		               'NO2': {'NC1': 0.0, 'NC0': 0.0}}
		print(helper.getNonControlledOffsetsFromProductID(qhawax_name))
		self.assertAlmostEqual(helper.getNonControlledOffsetsFromProductID(qhawax_name),offset_sensor)

	def test_query_get_non_controlled_offsets_from_productID_not_valid(self):
		self.assertRaises(TypeError,helper.getNonControlledOffsetsFromProductID,4)
		self.assertRaises(TypeError,helper.getNonControlledOffsetsFromProductID,None)
		self.assertRaises(TypeError,helper.getNonControlledOffsetsFromProductID,"342")



if __name__ == '__main__':
    unittest.main(verbosity=2)
