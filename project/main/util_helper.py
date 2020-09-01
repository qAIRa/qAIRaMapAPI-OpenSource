import datetime
import dateutil
import dateutil.parser
import time
import json

pollutant=['SO2','NO2','O3','CO','H2S']
pollutant_15C=[2.71,1.95,2.03,1.18,1.44]
pollutant_20C=[2.66,1.91,2.00,1.16,1.41]
pollutant_25C=[2.62,1.88,1.96,1.15,1.39]


def getCompanyTargetofJson(data):
    if 'company_name' not in data:
        raise ValueError("No target company_name in given json")
    if 'email_group' not in data:
        raise ValueError("No target email_group in given json")
    if 'ruc' not in data:
        raise ValueError("No target ruc in given json")
    if 'address' not in data:
        raise ValueError("No target address in given json")
    if 'phone' not in data:
        raise ValueError("No target phone in given json")
    if 'contact_person' not in data:
        raise ValueError("No target contact_person in given json")

def getOffsetTargetofJson(data):
    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'offsets' not in data:
        raise ValueError("No target offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

def getControlledOffsetTargetofJson(data):
    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'controlled_offsets' not in data:
        raise ValueError("No target controlled_offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

def getNonControlledOffsetTargetofJson(data):
    if 'product_id' not in data:
        raise ValueError("No target product_id in given json")
    if 'non_controlled_offsets' not in data:
        raise ValueError("No target non_controlled_offsets in given json")
    if 'description' not in data:
        raise ValueError("No target description in given json")
    if 'person_in_charge' not in data:
        raise ValueError("No target person_in_charge in given json")

def getValidTime(minutes_diff, date_util):
    if(is_intance(minutes_diff) is not [int]):
        raise TypeError("Variable "+str(minutes_diff)+" should be integer")

    if(minutes_diff<5):
        return date_util + datetime.timedelta(minutes=10)
    return date_util + datetime.timedelta(hours=2)

def getAverage(resultado):
    sum = 0        

    if len(resultado) == 0 :
        return 0
    else :
        for i in range(len(resultado)):
            sum = sum + resultado[i][0]
        promf = sum /len(resultado)

    return promf

def gasSensorJson(json,sensors):
    all_sensors=['CO','SO2','H2S','O3','NO','NO2']
    
    initial = {}

    for sensor in all_sensors:
        initial[sensor] = json

    for sensor in sensors:
        sensor_dict = sensor._asdict()
        initial[sensor_dict.pop('type')] = sensor_dict

    return initial

def getColorBaseOnIncaValue(qhawax_inca):
    if qhawax_inca == 50:
        resultado = 'green'
    elif qhawax_inca == 100:
        resultado = 'yellow'
    elif qhawax_inca == 500:
        resultado = 'orange'
    elif qhawax_inca == 600:
        resultado = 'red'
    else:
        resultado = 'green'
    return resultado

def validAndBeautyJsonProcessed(data_json):
    arr_season=[2.62,1.88,1.96,1.15,1.39] #Arreglo de 25C 
    data_json = checkNumberValues(data_json)
    data_json = gasConversionPPBtoMG(data_json, arr_season)
    data_json = roundUpThree(data_json)   
    data_json["timestamp_zone"] = data_json["timestamp"]
    return data_json

def gasConversionPPBtoMG(data_json,season):
    data={'ID': data_json['ID'],'CO': data_json['CO'], 'CO_ug_m3': 0,'H2S': data_json['H2S'],'H2S_ug_m3': 0,
          'NO2': data_json['NO2'],'NO2_ug_m3': 0,'O3': data_json['O3'],'O3_ug_m3': 0, 'PM1': data_json['PM1'],
          'PM10': data_json['PM10'],'PM25': data_json['PM25'],'SO2': data_json['SO2'],'SO2_ug_m3': 0,
          'spl': data_json['spl'],'UV': data_json['UV'],'UVA': data_json['UVA'],'UVB': data_json['UVB'],
          'humidity': data_json['humidity'],'lat':data_json['lat'],'lon':data_json['lon'],
          'pressure': data_json['pressure'],'temperature': data_json['temperature'],'timestamp': data_json['timestamp']}

    for key in data:
        if(key in pollutant):
            if(key=='SO2'):
                data['SO2_ug_m3']=data[key]*season[0]
            elif(key=='NO2'):
                data['NO2_ug_m3']=data[key]*season[1]
            elif(key=='O3'):
                data['O3_ug_m3']=data[key]*season[2]
            elif(key=='CO'):
                data['CO_ug_m3']=data[key]*season[3]
            elif(key=='H2S'):
                data['H2S_ug_m3']=data[key]*season[4]
    return data

def roundUpThree(data_json):
    data_json['CO']= round(data_json['CO'],3)
    data_json['CO_ug_m3']= round(data_json['CO_ug_m3'],3)
    data_json['H2S']= round(data_json['H2S'],3)
    data_json['H2S_ug_m3']= round(data_json['H2S_ug_m3'],3)
    data_json['NO2']= round(data_json['NO2'],3)
    data_json['NO2_ug_m3']= round(data_json['NO2_ug_m3'],3)
    data_json['O3']= round(data_json['O3'],3)
    data_json['O3_ug_m3']= round(data_json['O3_ug_m3'],3)
    data_json['PM1']= round(data_json['PM1'],3)
    data_json['PM10']= round(data_json['PM10'],3)
    data_json['PM25']= round(data_json['PM25'],3)
    data_json['SO2']= round(data_json['SO2'],3)
    data_json['SO2_ug_m3']= round(data_json['SO2_ug_m3'],3)
    data_json['spl']= round(data_json['spl'],3)
    data_json['UV']= round(data_json['UV'],3)
    data_json['humidity']= round(data_json['humidity'],3)
    data_json['pressure']= round(data_json['pressure'],3)
    return data_json

def averageMeasurementsInHours(measurements, initial_timestamp, final_timestamp, interval_hours):
    initial_hour_utc = initial_timestamp.astimezone(tz=dateutil.tz.tzutc()).replace(tzinfo=None)
    final_hour_utc = final_timestamp.astimezone(tz=dateutil.tz.tzutc()).replace(tzinfo=None)
    initial_hour = initial_hour_utc.replace(minute=0, second=0, microsecond=0)
    final_hour = final_hour_utc.replace(minute=0, second=0, microsecond=0)

    current_hour = initial_hour
    ind = 0
    measurements_in_timestamp = []
    averaged_measurements = []
    while current_hour < final_hour:
        if ind > len(measurements) - 1:
            break
        
        timestamp = measurements[ind]['timestamp']
        if timestamp >= current_hour and timestamp <= current_hour + datetime.timedelta(hours=interval_hours):
            measurements_in_timestamp.append(measurements[ind])
            ind += 1
        else:
            if len(measurements_in_timestamp) != 0:
                averaged_measurement = averageMeasurements(measurements_in_timestamp)
                averaged_measurement['timestamp'] = current_hour
                averaged_measurements.append(averaged_measurement)
            measurements_in_timestamp = []
            current_hour += datetime.timedelta(hours=interval_hours)
    
    if len(measurements_in_timestamp) != 0:
        averaged_measurement = averageMeasurements(measurements_in_timestamp)
        averaged_measurement['timestamp'] = current_hour
        averaged_measurements.append(averaged_measurement)

    return averaged_measurements


def averageMeasurements(measurements):
    SKIP_KEYS = ['timestamp', 'lat', 'lon']

    average_measurement = {}

    for sensor_name in measurements[0]:
        if sensor_name in SKIP_KEYS:
            continue
        
        sensor_values = [measurement[sensor_name] for measurement in measurements]
        if all([value is None for value in sensor_values]):
            average_measurement[sensor_name] = None
        else:
            sensor_values_without_none = [value for value in sensor_values if value is not None]
            average_measurement[sensor_name] = sum(sensor_values_without_none)/len(sensor_values_without_none)

    average_measurement['timestamp'] = measurements[-1]['timestamp']
    average_measurement['lat'] = measurements[-1]['lat']
    average_measurement['lon'] = measurements[-1]['lon']

    return average_measurement

def checkNumberValues(data_json):
    """
    Helper Processed Measurement function to check number values

    :type data_json: json
    :param data_json: json of measurement

    """
    if(data_json["temperature"]=="Nan"):
        data_json["temperature"] = 0

    if(data_json["pressure"]=="Nan"):
        data_json["pressure"] = 0

    if(data_json["humidity"]=="Nan"):
        data_json["humidity"] = 0

    if(data_json["spl"]=="Nan"):
        data_json["spl"] = 0

    if(data_json["UV"]=="Nan"):
        data_json["UV"] = 0

    if(data_json["UVA"]=="Nan"):
        data_json["UVA"] = 0

    if(data_json["UVB"]=="Nan"):
        data_json["UVB"] = 0

    if(data_json["CO"]=="Nan"):
        data_json["CO"] = 0

    if(data_json["H2S"]=="Nan"):
        data_json["H2S"] = 0

    if(data_json["NO2"]=="Nan"):
        data_json["NO2"] = 0

    if(data_json["O3"]=="Nan"):
        data_json["O3"] = 0

    if(data_json["SO2"]=="Nan"):
        data_json["SO2"] = 0

    if(data_json["PM1"]=="Nan"):
        data_json["PM1"] = 0

    if(data_json["PM25"]=="Nan"):
        data_json["PM25"] = 0

    if(data_json["PM10"]=="Nan"):
        data_json["PM10"] = 0

    return data_json

def checkNegatives(data_json):
    """
    Helper Processed Measurement function to valid negatives values

    :type data_json: json
    :param data_json: json of measurement

    """
    if(data_json["temperature"]<0):
        data_json["temperature"] = 0

    if(data_json["pressure"]<0):
        data_json["pressure"] = 0

    if(data_json["humidity"]<0):
        data_json["humidity"] = 0

    if(data_json["spl"]<0):
        data_json["spl"] = 0

    if(data_json["UV"]<0):
        data_json["UV"] = 0

    if(data_json["UVA"]<0):
        data_json["UVA"] = 0

    if(data_json["UVB"]<0):
        data_json["UVB"] = 0

    if(data_json["CO"]<0):
        data_json["CO"] = 0

    if(data_json["H2S"]<0):
        data_json["H2S"] = 0

    if(data_json["NO2"]<0):
        data_json["NO2"] = 0

    if(data_json["O3"]<0):
        data_json["O3"] = 0

    if(data_json["SO2"]<0):
        data_json["SO2"] = 0

    if(data_json["PM1"]<0):
        data_json["PM1"] = 0

    if(data_json["PM25"]<0):
        data_json["PM25"] = 0

    if(data_json["PM10"]<0):
        data_json["PM10"] = 0

    return data_json

def areFieldsValid(data):
    if(data['lat']=='' or data['lat']==None):
        return False

    if(data['lon']=='' or data['lon']==None):
        return False

    if(data['comercial_name']=='' or data['comercial_name']==None):
        return False

    if(data['company_id']=='' or data['company_id']==None):
        return False

    if(data['eca_noise_id']=='' or data['eca_noise_id']==None):
        return False

    if(data['qhawax_id']=='' or data['qhawax_id']==None):
        return False

    if(data['connection_type']=='' or data['connection_type']==None):
        return False

    if(data['season']=='' or data['season']==None):
        return False

    if(data['is_public']=='' or data['is_public']==None):
        return False

    if(data['person_in_charge']=='' or data['person_in_charge']==None):
        return False

    return True