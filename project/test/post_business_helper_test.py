import unittest

import project.main.business.post_business_helper as post_business_helper

class TestPostBusinessHelper(unittest.TestCase):
	"""
	Test of Post Business Functions

	"""
	def test_update_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,None,None)
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateOffsetsFromProductID,80)

	def test_update_controlled_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,None,None)
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateControlledOffsetsFromProductID,80)

	def test_update_non_controlled_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID)
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,None, None)
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateNonControlledOffsetsFromProductID,80)

	def test_update_main_inca_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable, None,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,50)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,100,None)

	def test_update_main_inca_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable, None,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,50)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,100,None)

	def test_save_status_off_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxTable)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxTable,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxTable,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxTable,100.0)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxTable,True)

	def test_save_status_off_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,"2020-08-01 00:00:00")
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,None,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,50,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,100,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,True)

	def test_save_status_on_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveStatusOnTable)
		self.assertRaises(TypeError,post_business_helper.saveStatusOnTable,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOnTable,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOnTable,True)

	def test_save_turn_on_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,None)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,50)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,True)

	def test_save_turn_on_after_calibration_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,None)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,50)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,True)

	def test_set_occupied_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.setOccupiedQhawax)
		self.assertRaises(TypeError,post_business_helper.setOccupiedQhawax,None)
		self.assertRaises(TypeError,post_business_helper.setOccupiedQhawax,"50")
		self.assertRaises(TypeError,post_business_helper.setOccupiedQhawax,True)

	def test_set_mode_customer_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.setModeCustomer)
		self.assertRaises(TypeError,post_business_helper.setModeCustomer,None)
		self.assertRaises(TypeError,post_business_helper.setModeCustomer,"50")
		self.assertRaises(TypeError,post_business_helper.setModeCustomer,True)

	def test_save_end_date_work_field_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,None)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,"50")
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,True)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,8)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,None, None)

	def test_set_available_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.setAvailableQhawax)
		self.assertRaises(TypeError,post_business_helper.setAvailableQhawax,None)
		self.assertRaises(TypeError,post_business_helper.setAvailableQhawax,"50")
		self.assertRaises(TypeError,post_business_helper.setAvailableQhawax,True)

	def test_change_mode_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.changeMode)
		self.assertRaises(TypeError,post_business_helper.changeMode,None)
		self.assertRaises(TypeError,post_business_helper.changeMode,5,"Cliente")
		self.assertRaises(TypeError,post_business_helper.changeMode,None,None)
		self.assertRaises(TypeError,post_business_helper.changeMode,"qH050",None)
		self.assertRaises(TypeError,post_business_helper.changeMode,None,"Cliente")
		self.assertRaises(TypeError,post_business_helper.changeMode,True)
		self.assertRaises(TypeError,post_business_helper.changeMode,True,"Cliente")

	def test_update_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,None)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,5)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,"qH050")
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,True)
		self.assertRaises(Exception,post_business_helper.updateQhawaxInstallation,{"hola":"hola"})

	def test_create_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.createQhawax)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None, None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None, None, None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,50, "qH050")
		self.assertRaises(TypeError,post_business_helper.createQhawax,"qH050","AEREAL")
		self.assertRaises(TypeError,post_business_helper.createQhawax,50,"AEREAL")
		self.assertRaises(TypeError,post_business_helper.createQhawax,"50","qH050","AEREAL")
		self.assertRaises(Exception,post_business_helper.createQhawax,50,"qH050",50)

	def test_insert_default_offsets_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,None)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,None, None)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,"1", "qH001")
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,50,100)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,"1",50)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,50,None)
		self.assertRaises(TypeError,post_business_helper.insertDefaultOffsets,True,"qH001")

	def test_create_company_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.createCompany)
		self.assertRaises(TypeError,post_business_helper.createCompany,4)
		self.assertRaises(TypeError,post_business_helper.createCompany,None)
		self.assertRaises(TypeError,post_business_helper.createCompany,"PUCP")
		self.assertRaises(TypeError,post_business_helper.createCompany,True)
		self.assertRaises(TypeError,post_business_helper.createCompany,{},4.0)

	def test_store_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,None)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,5)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,"qH050")
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,True)
		self.assertRaises(Exception,post_business_helper.storeNewQhawaxInstallation,{"hola":"hola"})

	def test_write_binnacle_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.writeBinnacle)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,4)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004",4,"l.montalvo")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004","Se apago el qHAWAX")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,80)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,80,None,None)
	

if __name__ == '__main__':
    unittest.main(verbosity=2)
