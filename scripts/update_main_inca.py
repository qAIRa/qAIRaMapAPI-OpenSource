import requests
import math
import datetime
import dateutil.parser
from passlib.hash import bcrypt
import json

BASE_URL = 'https://qairamapnapi-dev-opensource.qairadrones.com/'
#BASE_URL = 'http://0.0.0.0:5000/'
MAININCA_DATA_ENDPOINT = 'api/save_main_inca/'
GET_MEASUREMENT_PROM = 'api/measurementPromedio/'
GET_ACTIVE_QHAWAX_IN_FIELD = 'api/get_qhawaxs_active_mode_customer/'
SAVE_GAS_INCA_ENDPOINT = 'api/saveGasInca/'
GET_TIME_BY_QHAWAX_ACTIVE = 'api/get_time_all_active_qhawax/'
GET_TIMESTAMP_OF_VALID = 'api/get_time_valid_data_active_qhawax/'

def init_inca_gas_processed(sensor_array,value_sensor_array, calInca):
    inca_json = {}
    starting_hour = datetime.datetime.now(dateutil.tz.tzutc())
    inca_json['timestamp_zone'] = str(starting_hour.replace(minute=0, second=0, microsecond=0))
    for i in range(len(value_sensor_array)):
        inca_json[sensor_array[i]] = value_sensor_array[i]
    
    inca_json['CO2'] = 0.0
    inca_json['NO'] = 0.0
    inca_json['PM1'] = 0.0
    inca_json['main_inca'] = calInca
    
    return inca_json

def validaH2S(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=1000:
        calificacionInca = 500
    elif val >1000:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

def validaCO_NO2(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=150:
        calificacionInca = 500
    elif val >150:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

def validaSO2(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=625:
        calificacionInca = 500
    elif val >625:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

def validaPM10(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=167:
        calificacionInca = 500
    elif val >167:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

def validaPM25(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=500:
        calificacionInca = 500
    elif val >500:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

def validaO3(val):
    calificacionInca = 0
    if val >=0 and val<= 50 :
        calificacionInca = 50
    elif val >50 and val<=100:
        calificacionInca = 100
    elif val >100 and val<=175:
        calificacionInca = 500
    elif val >175:
        calificacionInca = 600
    else:
        calificacionInca = -1

    return calificacionInca

factor_final_CO = (0.0409 * 28.01 * 100)/10000
factor_final_NO2 = (0.0409 * 46.0055 * 100)/200
factor_final_PM10 = 100/150
factor_final_PM25 = 100/25
factor_final_SO2 = (0.0409 * 64.066 * 100)/20
factor_final_O3 = (0.0409 * 48* 100)/120
factor_final_H2S = (0.0409 * 34.1*100)/150

def setFactorArray():
    array = []
    array.append(factor_final_CO)
    array.append(factor_final_NO2)
    array.append(factor_final_PM10)
    array.append(factor_final_PM25)
    array.append(factor_final_SO2)
    array.append(factor_final_O3)
    array.append(factor_final_H2S)
    return array

def verifySensor(responseSensor,factor_final_sensor,sensor_type):
    valueSensor = None
    if(responseSensor.text!="-1"):
        valueSensor = math.floor(float(responseSensor.text) * factor_final_sensor)
        if(sensor_type == 'NO2' or sensor_type == 'CO')
            aux = validaCO_NO2(valueSensor)

        if(sensor_type == 'H2S')
            aux = validaH2S(valueSensor)

        if(sensor_type == 'SO2')
            aux = validaSO2(valueSensor)

        if(sensor_type == 'PM10')
            aux = validaPM10(valueSensor)

        if(sensor_type == 'PM25')
            aux = validaPM25(valueSensor)

        if(sensor_type == 'O3')
            aux = validaO3(valueSensor)
    return aux,valueSensor

# Request all qhawax
fator_array = setFactorArray()
response = requests.get(BASE_URL + GET_ACTIVE_QHAWAX_IN_FIELD)
qhawax_names = [qhawax['name'] for qhawax in response.json()]
for qhawax_name in qhawax_names:
    try:
        print("Qhawax: "+ str(qhawax_name))
        values = json.loads((requests.get(BASE_URL + GET_TIME_BY_QHAWAX_ACTIVE, params={'name': qhawax_name})).text)
        last_time_turn_on= dateutil.parser.parse(values['last_time_on'])
        last_time_registration = dateutil.parser.parse(values['last_time_registration'])
        if(last_time_registration <= last_time_turn_on):
            print("Entre a last_time < a last_time_turn_on: "+ str(qhawax_name))
            minutes_diff =  int((last_time_turn_on - last_time_registration).total_seconds() / 60)
            valid_response_time = dateutil.parser.parse((requests.get(BASE_URL + GET_TIMESTAMP_OF_VALID, params={'name': qhawax_name})).text)
            if(valid_response_time!=None):
                print("Entre a valid_response_time no es NONE "+ str(qhawax_name))
                if(valid_response_time.replace(tzinfo=None) >= last_time_turn_on.replace(tzinfo=None)):
                    print("Entre a valid_response_time >= a last_time_turn_on "+ str(qhawax_name))

                    sensor_array = ['CO','NO2','PM10','PM25','SO2','O3','H2S']
                    hour_array = [8,1,24,24,24,8,24]
                    response_array = []
                    value_sensor_array = []
                    for sensor_i in range(len(sensor_array)):
                        response_sensor = requests.get(BASE_URL + GET_MEASUREMENT_PROM, params={'name': qhawax_name, 'sensor': sensor_array[i], 'hoursSensor': hour_array[i],'minutes_diff':minutes_diff, 'last_time_turn_on':last_time_turn_on})
                        response_array.append(response_sensor)

                    aux = 0
                    calInca = 0
                    for i in range(len(sensor_array)):
                        aux,valueSensor =verifySensor(response_array[i],factor_array[i],sensor_array[i])
                        value_sensor_array.append(valueSensor)
                        if aux > calInca:
                            calInca = aux
                           
                    name_qhawax = qhawax_name
                    inca_gas_processed = init_inca_gas_processed(sensor_array,value_sensor_array,calInca)
                
                    inca_gas_processed['ID'] = qhawax_name
                    if(calInca!=0):
                        print("Entre a cal inca !=0 :"+ str(qhawax_name))
                        response = requests.post(BASE_URL + SAVE_GAS_INCA_ENDPOINT, json=inca_gas_processed)
                        response = requests.post(BASE_URL + MAININCA_DATA_ENDPOINT, json ={'name': name_qhawax, 'value_inca': calInca})
            
    except Exception as e:
        print(e)
