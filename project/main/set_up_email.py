
def set_email_text(email_type, comercial_name, qhawax_name, mode,timestamp):
	json_email = {}
	json_email['observation_type']="Interna"
	json_email['person_in_charge']="Firmware"
	if(email_type=="qHAWAX restart"):
		json_email['description']="Se prendió el qHAWAX luego de un reinicio general"
		json_email['subject'] = 'qHAWAX ( %s ) se encendió ' % (comercial_name)
		json_email['content1'] = 'qHAWAX %s mandó señal de prendido' % (qhawax_name) 
		content2 = '\nSe han reiniciado los sensores'
		content3 = '\nqHAWAX en modo: %s' % (mode)
		json_email['content2'] = content2 + content3
	elif(email_type == "qHAWAX signal"):
		json_email['description']="Se prendió el qHAWAX luego de una pérdida de señal"
		json_email['subject'] = 'qHAWAX ( %s ) recuperó señal' % (comercial_name)
		json_email['content1'] = 'qHAWAX %s' % (qhawax_name)
		content2 = '\nRecuperó señal: %s \nLuego de perder conexión o señal de internet' % (timestamp)
		content3 = '\nqHAWAX en modo: %s' % (mode)
		json_email['content2'] = content2 + content3
	elif(email_type == "qHAWAX loop"):
		json_email['subject'] = 'qHAWAX ( %s ) entró en loop' % (comercial_name)
		json_email['content1'] = 'qHAWAX %s' % (qhawax_name)
		content2 = '\n El qHAWAX ha mandado señal de prendido 20 veces, sin apagarse'
		content3 = '\n Hora de inicio del loop: %s' % (timestamp)
		json_email['content2'] = content2 + content3
	elif(email_type == "qHAWAX off"):
		json_email['description']="Se apagó el qHAWAX"
		json_email['person_in_charge'] = "Server/Web"
	elif(email_type == "qHAWAX off alert"):
		json_email['subject'] = 'qHAWAX: %s Inactivo' % (comercial_name)
		json_email['content1'] = 'qHAWAX %s' % (qhawax_name)
		content2 = '\nUltima vez que se mostró activo (Lima - Peru): %s' % (timestamp)
		json_email['content2'] = content2  
	elif(email_type == "qHAWAX processed"):
		json_email['description']="Se prendió el qHAWAX sin enviar señal"
		json_email['subject'] = 'qHAWAX: %s Recuperó Señal' % (comercial_name)
		json_email['content1'] = 'qHAWAX %s se prendió, pero no envió señal' % (qhawax_name)
		content2 = '\nRecuperó señal (Lima - Peru): %s' % (timestamp)
		json_email['content2'] = content2 
		json_email['person_in_charge'] = "API"
	return json_email