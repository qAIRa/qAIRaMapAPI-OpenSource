import unittest
import datetime
from datetime import timedelta
import dateutil
import dateutil.parser
import project.main.business.post_business_helper as post_business_helper
import project.main.business.get_business_helper as get_business_helper
from random import randint

class TestPostBusinessHelper(unittest.TestCase):
	""" Test of Post Business Functions """
	def test_update_gas_sensor_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor)
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,None,None)
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,None,{"offset":{}})
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,"qH080",True)
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateJsonGasSensor,80)

	def test_update_gas_sensor_valid(self):
		offset = {"CO":{"AE":1.0,"WE":337.0,"sensitivity":0.45,"sensitivity_2":0.0}, 
				  "H2S":{"AE":1.0,"WE":350.0,"sensitivity":1.724,"sensitivity_2":0.0}, 
				  "NO":{"AE":1.0,"WE":300.0,"sensitivity":0.3,"sensitivity_2":0.0}, 
				  "NO2":{"AE":235.0,"WE":228.0,"sensitivity":0.234,"sensitivity_2":0.0},	
				  "O3":{"AE":120.0,"WE":224.0,"sensitivity":0.326,"sensitivity_2":0.0},
				  "SO2":{"AE":320.0,"WE":346.0,"sensitivity":0.37,"sensitivity_2":0.0}}
		controlled_offset = {"CO":{"C0":17.0,"C1":1.0,"C2":0.0}, 
							  "H2S":{"C0":17.0,"C1":1.0,"C2":0.0}, 
							  "NO":{"C0":24.0,"C1":1.0,"C2":0.0}, 
							  "NO2":{"C0":50.0,"C1":1.0,"C2":0.0},	
							  "O3":{"C0":20.0,"C1":1.0,"C2":0.0},
							  "SO2":{"C0":0.0,"C1":1.0,"C2":0.0}}
		non_controlled_offset = {"CO":{"NC0":19.0,"NC1":0.0}, 
								  "H2S":{"NC0":20.0,"NC1":0.0}, 
								  "NO":{"NC0":21.0,"NC1":0.0}, 
								  "NO2":{"NC0":0.0,"NC1":17.0},	
								  "O3":{"NC0":0.0,"NC1":18.0},
								  "SO2":{"NC0":0.0,"NC1":19.0}}
		post_business_helper.updateJsonGasSensor('qH035',offset)
		post_business_helper.updateJsonGasSensor('qH035',controlled_offset)
		post_business_helper.updateJsonGasSensor('qH035',non_controlled_offset)

	def test_update_main_inca_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable, None,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,50)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxTable,100,None)

	def test_update_main_inca_qhawax_valid(self):
		post_business_helper.updateMainIncaQhawaxTable(-1,'qH035')

	def test_update_main_inca_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,"qH080",None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable, None,"qH080")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,"qH004")
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,None)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,50)
		self.assertRaises(TypeError,post_business_helper.updateMainIncaQhawaxInstallationTable,100,None)

	def test_update_main_inca_qhawax_installation_valid(self):
		post_business_helper.updateMainIncaQhawaxInstallationTable(-1,'qH004')

	def test_save_status_off_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveStatusQhawaxTable)
		self.assertRaises(TypeError,post_business_helper.saveStatusQhawaxTable,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusQhawaxTable,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusQhawaxTable,100.0)
		self.assertRaises(TypeError,post_business_helper.saveStatusQhawaxTable,True)

	def test_save_status_off_qhawax_valid(self):
		post_business_helper.saveStatusQhawaxTable('qH035','ON',0)
		post_business_helper.saveStatusQhawaxTable('qH035','OFF',-1)

	def test_save_status_off_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,"2020-08-01 00:00:00")
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,None,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,50,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,50)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,100,None)
		self.assertRaises(TypeError,post_business_helper.saveStatusOffQhawaxInstallationTable,True)

	def test_save_status_off_qhawax_installation_valid(self):
		initial_timestamp = "27-09-2020 00:00:00.877701+00:00"
		date_format = '%d-%m-%Y %H:%M:%S.%f%z'
		last_time_turn_on = datetime.datetime.strptime(initial_timestamp,date_format)
		post_business_helper.saveStatusOffQhawaxInstallationTable('qH004',last_time_turn_on)

	def test_save_turn_on_qhawax_installation_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,None)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,50)
		self.assertRaises(TypeError,post_business_helper.saveTurnOnLastTime,True)

	#def test_save_turn_on_qhawax_installation_valid(self):
		#post_business_helper.saveTurnOnLastTime('qH004')

	def test_save_turn_on_after_calibration_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,None)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,50)
		self.assertRaises(TypeError,post_business_helper.turnOnAfterCalibration,True)

	def test_set_occupied_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.setAvailabilityQhawax)
		self.assertRaises(TypeError,post_business_helper.setAvailabilityQhawax,None)
		self.assertRaises(TypeError,post_business_helper.setAvailabilityQhawax,"qH004")
		self.assertRaises(TypeError,post_business_helper.setAvailabilityQhawax,True)

	def test_set_occupied_qhawax_valid(self):
		post_business_helper.setAvailabilityQhawax(4,'Available')
		post_business_helper.setAvailabilityQhawax(4,'Occupied')

	def test_save_end_date_work_field_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,None)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,"50")
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,True)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,8)
		self.assertRaises(TypeError,post_business_helper.saveEndWorkFieldDate,None, None)

	def test_change_mode_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.changeMode)
		self.assertRaises(TypeError,post_business_helper.changeMode,None)
		self.assertRaises(TypeError,post_business_helper.changeMode,5,"Cliente")
		self.assertRaises(TypeError,post_business_helper.changeMode,None,None)
		self.assertRaises(TypeError,post_business_helper.changeMode,"qH050",None)
		self.assertRaises(TypeError,post_business_helper.changeMode,None,"Cliente")
		self.assertRaises(TypeError,post_business_helper.changeMode,True)
		self.assertRaises(TypeError,post_business_helper.changeMode,True,"Cliente")

	def test_change_mode_valid(self):
		post_business_helper.changeMode("qH001","Stand By")

	def test_update_qhawax_installation_not_valid(self):
		installation_json = {'lat':None,'lon':None,'comercial_name':None,
							 'company_id':1,'eca_noise_id':1,'qhawax_id':100,
							 'connection_type':None,'season':'Primavera','is_public':None,
							 'person_in_charge':None}
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,None)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,5)
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,"qH050")
		self.assertRaises(TypeError,post_business_helper.updateQhawaxInstallation,True)
		self.assertRaises(Exception,post_business_helper.updateQhawaxInstallation,installation_json)

	def test_update_qhawax_installation_valid(self):
		installation_json = {'lat':'-12.0000499','lon':'-77.9000000','comercial_name':'Unit Test Coveralls',
							 'company_id':1,'eca_noise_id':1,'qhawax_id':15,'connection_type':'Panel Solar',
							 'season':'Primavera','is_public':'no','person_in_charge':'l.montalvo'}
		post_business_helper.updateQhawaxInstallation(installation_json)

	def test_create_qhawax_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.createQhawax)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None, None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,None, None, None)
		self.assertRaises(TypeError,post_business_helper.createQhawax,50,"AEREAL")
		self.assertRaises(Exception,post_business_helper.createQhawax,"qH050",50)

	def test_create_qhawax_and_default_sensors_valid(self):
		end_date_string = "2020-10-30 00:00:00.255258"
		date_format = '%Y-%m-%d %H:%M:%S.%f'
		person_in_charge = 'l.montalvo'
		last_qhawax_id = int(get_business_helper.queryGetLastQhawax()[0]) +1
		qhawax_name = 'qH0'+str(last_qhawax_id)
		post_business_helper.createQhawax(qhawax_name,'STATIC')
		last_gas_sensor_id = int(get_business_helper.queryGetLastGasSensor()[0]) +1
		post_business_helper.insertDefaultOffsets(qhawax_name)
		installation_json = {'lat':'-12.0000499','lon':'-77.9000000',
							 'comercial_name':'Unit Test '+str(randint(0, 20))+' Coveralls',
							 'company_id':1,'eca_noise_id':1,'qhawax_id':int(last_qhawax_id),
							 'connection_type':'Panel Solar','season':'Primavera','is_public':'no',
							 'person_in_charge':person_in_charge}
		post_business_helper.storeNewQhawaxInstallation(installation_json)
		description = 'qHAWAX record in field'
		post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
		post_business_helper.saveEndWorkFieldDate(last_qhawax_id,end_date_string,date_format)
		description = 'qHAWAX save end work in field'
		post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)

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

	def test_create_company_valid(self):
		json= {"company_name": "Unit Test "+str(randint(0, 20))+"_"+str(randint(0, 20)), "email_group": "unitest"+str(randint(0, 20))+"-"+str(randint(0, 20))+".gob",
			   "ruc":"12345678"+str(randint(200, 900)),"phone":"998123123","contact_person":"Test","address":"Prueba"}
		post_business_helper.createCompany(json)

	def test_store_qhawax_installation_not_valid(self):
		installation_json = {'lat':None,'lon':None,'comercial_name':None,
							 'company_id':1,'eca_noise_id':1,'qhawax_id':100,
							 'connection_type':None,'season':'Primavera','is_public':None,
							 'person_in_charge':None}
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,None)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,5)
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,"qH050")
		self.assertRaises(TypeError,post_business_helper.storeNewQhawaxInstallation,True)
		self.assertRaises(Exception,post_business_helper.storeNewQhawaxInstallation,installation_json)

	def test_write_binnacle_not_valid(self):
		self.assertRaises(TypeError,post_business_helper.writeBinnacle)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,80,"description","l.montalvo")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,None)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH080",None,4)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004",4,"l.montalvo")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004","Se apago el qHAWAX")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004","description",True)
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,"qH004")
		self.assertRaises(TypeError,post_business_helper.writeBinnacle,None)
	
if __name__ == '__main__':
    unittest.main(verbosity=2)
