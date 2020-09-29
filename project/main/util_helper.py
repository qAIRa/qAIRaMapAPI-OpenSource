import datetime
from datetime import timedelta
import dateutil
import dateutil.parser

pollutant=['SO2','NO2','O3','CO','H2S']
pollutant_15C=[2.71,1.95,2.03,1.18,1.44]
pollutant_20C=[2.66,1.91,2.00,1.16,1.41]
pollutant_25C=[2.62,1.88,1.96,1.15,1.39]

array_ppb = ['CO','H2S','NO2','O3','SO2',\
             'PM1','PM10','PM25','spl','UV',\
             'UVA','UVB','humidity','pressure','temperature']

array_ug_m3 = ['CO','CO_ug_m3','H2S','H2S_ug_m3','NO2','NO2_ug_m3','O3',\
               'O3_ug_m3','PM1','PM10','PM25','SO2','SO2_ug_m3','spl','UV',\
               'humidity','pressure']

array_installation =['lat','lon','comercial_name','company_id','eca_noise_id','qhawax_id',\
                         'connection_type','season','is_public','person_in_charge']

def check_valid_date(date,date_format):
    """
    Check if it's a valid date.
    """
    if(isinstance(date, str) is not True):  
        raise TypeError("Variable "+str(date)+" should be string")
    try:
        date = datetime.datetime.strptime(date,date_format)
    except ValueError:
        raise ValueError("Date "+str(date)+" should be datetime "+str(date_format)+" Format")

def getValidTime(minutes_diff, date_util):
    if(isinstance(minutes_diff, int) is not True): 
        raise TypeError("Variable "+str(minutes_diff)+" should be integer")

    if(minutes_diff<5):
        return date_util + datetime.timedelta(minutes=10)
    return date_util + datetime.timedelta(hours=2)

def gasSensorJson(json,sensors):
    all_sensors=['CO','SO2','H2S','O3','NO','NO2']

    if(isinstance(json, dict) is not True):
        raise TypeError("json "+str(json)+" should be Json Format")

    if(isinstance(sensors, list) is not True):
        raise TypeError("sensors "+str(sensors)+" should be List Format")

    initial = {}

    for sensor in all_sensors:
        initial[sensor] = json

    for sensor in sensors:
        sensor_dict = sensor._asdict()
        initial[sensor_dict.pop('type')] = sensor_dict

    return initial

def getColorBaseOnIncaValue(qhawax_inca):
    if(isinstance(qhawax_inca, int) is not True):
        raise TypeError("qHAWAX Inca value "+str(qhawax_inca)+" should be integer")

    if qhawax_inca == 50:
        return 'green'
    elif qhawax_inca == 100:
        return'yellow'
    elif qhawax_inca == 500:
        return'orange'
    elif qhawax_inca == 600:
        return'red'
    return 'green'

def validTimeJsonProcessed(data_json):
    if(isinstance(data_json, dict) is not True):
        raise TypeError("json "+str(data_json)+" should be Json Format")

    datetime_array = data_json['timestamp'].split() 
    measurement_year = datetime.datetime.strptime(datetime_array[0], '%Y-%m-%d').year
    if(measurement_year > datetime.date.today().year):
        data_json['timestamp'] = (datetime.datetime.now(dateutil.tz.tzutc())-datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        data_json['timestamp_zone'] = (datetime.datetime.now(dateutil.tz.tzutc())).strftime("%Y-%m-%d %H:%M:%S")
    return data_json

def validAndBeautyJsonProcessed(data_json):
    arr_season=[2.62,1.88,1.96,1.15,1.39] #Arreglo de 25C 

    if(isinstance(data_json, dict) is not True):
        raise TypeError("json "+str(data_json)+" should be Json Format")

    if  'timestamp_zone' not in data_json:
        data_json["timestamp_zone"] = data_json["timestamp"]
    data_json = gasConversionPPBtoMG(data_json, arr_season)
    data_json = roundUpThree(data_json)
    return data_json

def gasConversionPPBtoMG(data_json,season):
    if(isinstance(data_json, dict) is not True):
        raise TypeError("json "+str(data_json)+" should be Json Format")

    if(isinstance(season, list) is not True):
        raise TypeError("season "+str(season)+" should be List Format")

    data={'ID': data_json['ID'],'CO': data_json['CO'], 'CO_ug_m3': 0,'H2S': data_json['H2S'],
          'H2S_ug_m3': 0,'NO2': data_json['NO2'],'NO2_ug_m3': 0,'O3': data_json['O3'],
          'O3_ug_m3': 0, 'PM1': data_json['PM1'],'PM10': data_json['PM10'],'PM25': data_json['PM25'],
          'SO2': data_json['SO2'],'SO2_ug_m3': 0,'spl': data_json['spl'],'UV': data_json['UV'],
          'UVA': data_json['UVA'],'UVB': data_json['UVB'],'humidity': data_json['humidity'],
          'lat':data_json['lat'],'lon':data_json['lon'],'pressure': data_json['pressure'],
          'temperature': data_json['temperature'],'timestamp': data_json['timestamp'],
          'timestamp_zone': data_json['timestamp_zone']}
    for key in data:
        if(key in pollutant):
            if((type(data[key]) is float) or (type(data[key]) is int)):
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
    if(isinstance(data_json, dict) is not True):
        raise TypeError("Measurement variable "+str(data_json)+" should be Json Format")

    for i in range(len(array_ug_m3)):
        data_json[array_ug_m3[i]] = round(data_json[array_ug_m3[i]],3)
    return data_json


def checkNumberValues(data_json):
    """
    Helper Processed Measurement function to check number values

    :type data_json: json
    :param data_json: json of measurement

    """
    if(isinstance(data_json, dict) is not True):
        raise TypeError("Measurement variable "+str(data_json)+" should be Json Format")
    for i in range(len(array_ppb)):
        if(data_json[array_ppb[i]]=="Nan"):
            data_json[array_ppb[i]] = 0
    return data_json

def checkNegatives(data_json):
    """
    Helper Processed Measurement function to valid negatives values

    :type data_json: json
    :param data_json: json of measurement

    """
    if(isinstance(data_json, dict) is not True):
        raise TypeError("Measurement variable "+str(data_json)+" should be Json Format")

    for i in range(len(array_ppb)):
        if(data_json[array_ppb[i]]<0):
            data_json[array_ppb[i]] = 0

    return data_json


def areFieldsValid(data):
    if(isinstance(data, dict) is not True):
        raise TypeError("qHAWAX installation variable "+str(data)+" should be Json Format")

    for i in range(len(array_installation)):
        if(data[array_installation[i]]=='' or data[array_installation[i]]==None):
            return False
    return True


def averageMeasurements(measurements):
    SKIP_KEYS = ['timestamp', 'lat', 'lon']

    if(isinstance(measurements, dict) is not True):
        raise TypeError("Measurement variable "+str(measurements)+" should be Json Format")

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

def getDateRangeFromWeek(p_year,p_week):
    """
    Helper to get date range from week

    :type p_year: integer
    :param p_year: year 

    :type p_week: integer
    :param p_week: week number

    """
    if(isinstance(p_year, int) is not True):
        raise TypeError("Year value "+str(p_year)+" should be integer")

    if(isinstance(p_week, int) is not True):
        raise TypeError("Week value "+str(p_week)+" should be integer")

    if(p_year<2020):
        raise ValueError("Year value "+str(p_year)+" should be higher or equal 2020")

    if(p_week<=0 and p_week>=54):
        raise ValueError("Week value "+str(p_week)+" should be higher than cero and lower than 54")

    d = str(p_year)+'-W'+str((int(p_week)- 1))+'-1'

    firstdayofweek = datetime.datetime.strptime(d, "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek


def getFormatData(gas_average_measurement):
    if(isinstance(gas_average_measurement, dict) is not True):
        raise TypeError("Gas Average Measurement variable "+str(gas_average_measurement)+" should be Json Format")

    gas_average_measurement_list = []
    if gas_average_measurement is not None:
        next_hour = -1
        for measurement in gas_average_measurement:
            gas_measurement = measurement._asdict() 
            hour = gas_measurement["timestamp_zone"].hour
            if(next_hour == -1): 
                gas_average_measurement_list.append(gas_measurement)
                next_hour = hour + 1
            else:
                if(hour == next_hour):
                    gas_average_measurement_list.append(gas_measurement)                   
                else:
                    if(next_hour>hour): # si next_hour > hour => se resta con 24 horas
                        diff_0 = abs(24 - next_hour) 
                        diff = diff_0 + hour 
                    else:
                        diff = abs(hour - next_hour-1)
                    for i in range(1,diff+1):
                        new_variable ={"timestamp_zone":before_date + datetime.timedelta(hours=i),"sensor":""}
                        gas_average_measurement_list.append(new_variable)
                    gas_average_measurement_list.append(gas_measurement)
                next_hour = hour + 1
            before_date = gas_measurement["timestamp_zone"]
            if(next_hour == 24): next_hour = 0
        return gas_average_measurement_list
    return None
