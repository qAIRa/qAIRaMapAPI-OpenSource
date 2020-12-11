import datetime
from datetime import timedelta
import dateutil
import dateutil.parser

pollutant=['SO2','NO2','O3','CO','H2S']

array_ppb = ['CO','H2S','NO2','O3','SO2','PM1','PM10','PM25','spl','UV',\
             'UVA','UVB','humidity','pressure','temperature']

array_ug_m3 = ['CO','CO_ug_m3','H2S','H2S_ug_m3','NO2','NO2_ug_m3','O3',\
               'O3_ug_m3','PM1','PM10','PM25','SO2','SO2_ug_m3','spl','UV',\
               'UVA','UVB','humidity','pressure']

array_installation =['lat','lon','comercial_name','company_id','eca_noise_id','qhawax_name',\
                         'connection_type','season','is_public','person_in_charge']

def check_valid_date(date,date_format):
    """ Check if it's a valid date. """
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
    #Convertir los pascales a hectopascales
    data_json['pressure']= float(data_json['pressure'])*0.01 if (data_json['pressure']!="Nan") else "Nan"
    data_json = roundUpThree(data_json)
    return data_json

def gasConversionPPBtoMG(data_json,season):
    if(isinstance(data_json, dict) is not True):
        raise TypeError("json "+str(data_json)+" should be Json Format")

    if(isinstance(season, list) is not True):
        raise TypeError("season "+str(season)+" should be List Format")

    data={'ID': data_json['ID'],'CO': data_json['CO'], 'CO_ug_m3': None,'H2S': data_json['H2S'],
          'H2S_ug_m3': None,'NO2': data_json['NO2'],'NO2_ug_m3': None,'O3': data_json['O3'],
          'O3_ug_m3': None, 'PM1': data_json['PM1'],'PM10': data_json['PM10'],'PM25': data_json['PM25'],
          'SO2': data_json['SO2'],'SO2_ug_m3': None,'spl': data_json['spl'],'UV': data_json['UV'],
          'UVA': data_json['UVA'],'UVB': data_json['UVB'],'humidity': data_json['humidity'],
          'lat':data_json['lat'],'lon':data_json['lon'],'pressure': data_json['pressure'],
          'temperature': data_json['temperature'],'timestamp': data_json['timestamp'],
          'timestamp_zone': data_json['timestamp_zone'],'VOC': data_json['VOC'] if ('VOC' in data_json) else None,
          'CO2': data_json['CO2'] if ('CO2' in data_json) else None,
          'I_temperature': data_json['I_temperature'] if ('I_temperature' in data_json) else None}

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
        if((type(data_json[array_ug_m3[i]]) is float) or (type(data_json[array_ug_m3[i]]) is int)):
            data_json[array_ug_m3[i]] = round(data_json[array_ug_m3[i]],3)
    return data_json

def checkNumberValues(data_json):
    """ Helper Processed Measurement function to check number values """
    if(isinstance(data_json, dict) is not True):
        raise TypeError("Measurement variable "+str(data_json)+" should be Json Format")
    for i in range(len(array_ppb)):
        if(data_json[array_ppb[i]]=="Nan"):
            data_json[array_ppb[i]] = 0
    return data_json

def checkNegatives(data_json):
    """ Helper Processed Measurement function to valid negatives values """
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

def getDateRangeFromWeek(p_year,p_week):
    """ Helper to get date range from week """
    if(isinstance(p_year, int) is not True):
        raise TypeError("Year value "+str(p_year)+" should be integer")

    if(isinstance(p_week, int) is not True):
        raise TypeError("Week value "+str(p_week)+" should be integer")

    if(p_year<2020):
        raise ValueError("Year value "+str(p_year)+" should be higher or equal 2020")

    if(p_week<=0 or p_week>=54):
        raise ValueError("Week value "+str(p_week)+" should be higher than cero and lower than 54")

    d = str(p_year)+'-W'+str((int(p_week)- 1))+'-1'

    firstdayofweek = datetime.datetime.strptime(d, "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek


def getFormatData(gas_average_measurement):
    if(isinstance(gas_average_measurement, list) is not True):
        raise TypeError("Gas Average Measurement variable "+str(gas_average_measurement)+" should be List Format")

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

def setNoneStringElements(data_json):
    string_fields = ['ID','timestamp_zone','timestamp','zone']
    for key in data_json:
        if((type(data_json[key]) is str) and (key not in string_fields)):
            data_json[key]=None
    return data_json

def NanToCeroJsonProcessed(data_json):
    return setNoneStringElements(data_json)

def getHoursPerSensor(sensor,air_quality_column):
    idx = -1
    if sensor == 'CO':
        idx = 0
    elif sensor == 'NO2':
        idx = 1
    elif sensor == 'PM10':
        idx = 2
    elif sensor == 'PM25':
        idx = 3
    elif sensor == 'SO2':
        idx = 4
    elif sensor == 'O3':
        idx = 5
    elif sensor == 'H2S':
        idx = 6
    return idx

def checkNoneValues(resultado):
    not_none_number = []
    for i in range(len(resultado)):
        if(resultado[i][0] is not None):
            not_none_number.append(resultado[i][0])
    return not_none_number

