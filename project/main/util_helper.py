import datetime
from datetime import timedelta

import dateutil
import dateutil.parser

import project.main.exceptions as exceptions

pollutant = ["SO2", "NO2", "O3", "CO", "H2S"]

array_ppb = [
    "CO",
    "H2S",
    "NO2",
    "O3",
    "SO2",
    "PM1",
    "PM10",
    "PM25",
    "spl",
    "UV",
    "UVA",
    "UVB",
    "humidity",
    "pressure",
    "temperature",
]

array_ug_m3 = [
    "CO",
    "CO_ug_m3",
    "H2S",
    "H2S_ug_m3",
    "NO2",
    "NO2_ug_m3",
    "O3",
    "O3_ug_m3",
    "PM1",
    "PM10",
    "PM25",
    "SO2",
    "SO2_ug_m3",
    "spl",
    "UV",
    "UVA",
    "UVB",
    "humidity",
    "pressure",
]

array_installation =['lat','lon','comercial_name','company_id','eca_noise_id','qhawax_name',\
                         'connection_type','is_public','person_in_charge'] # season not needed

# mobile qhawax specific constants to cover Lima
lat_lima_interval = [-12.67, -11.59]
lon_lima_interval = [-77.20, -76.75]


def validTimeJsonProcessed(data_json):
    data_json = exceptions.checkVariable_helper(data_json, dict)
    datetime_array = data_json["timestamp"].split()
    measurement_year = datetime.datetime.strptime(
        datetime_array[0], "%Y-%m-%d"
    ).year
    if measurement_year > datetime.date.today().year:
        data_json["timestamp"] = (
            datetime.datetime.now(dateutil.tz.tzutc())
            - datetime.timedelta(hours=5)
        ).strftime("%Y-%m-%d %H:%M:%S")
        data_json["timestamp_zone"] = (
            datetime.datetime.now(dateutil.tz.tzutc())
        ).strftime("%Y-%m-%d %H:%M:%S")
    return data_json


def validTimeJsonProcessedTest(data_json, time_zone, location_time_zone):
    datetime_timestamp = datetime.datetime.strptime(
        data_json["timestamp"], "%Y-%m-%d %H:%M:%S%z"
    )  # lo pasamos a utc 00
    local_time = (
        datetime.datetime.now() + datetime.timedelta(hours=time_zone)
    ).replace(microsecond=0)
    loc_dt = location_time_zone.localize(local_time)
    now_datetime = loc_dt + datetime.timedelta(minutes=2)
    now_datetime_past = loc_dt - datetime.timedelta(minutes=2)
    if (
        datetime_timestamp >= now_datetime
        or datetime_timestamp <= now_datetime_past
    ):
        return None
    return data_json


def validAndBeautyJsonProcessed(data_json):
    arr_season = [2.62, 1.88, 1.96, 1.15, 1.39]  # Arreglo de 25C
    data_json = exceptions.checkVariable_helper(data_json, dict)

    if "timestamp_zone" not in data_json:
        data_json["timestamp_zone"] = data_json["timestamp"]
    data_json = gasConversionPPBtoMG(data_json, arr_season)
    # Convertir los pascales a hectopascales
    data_json["pressure"] = (
        float(data_json["pressure"]) * 0.01
        if (data_json["pressure"] != "Nan")
        else "Nan"
    )
    data_json = roundUpThree(data_json)
    return data_json


# def validAndBeautyJsonProcessedLatest(data_json):
#     arr_season=[2.62,1.88,1.96,1.15,1.39] #Arreglo de 25C
#     data_json = exceptions.checkVariable_helper(data_json, dict)

#     if  'timestamp_zone' not in data_json:
#         data_json["timestamp_zone"] = data_json["timestamp"]
#     data_json = gasConversionPPBtoMG(data_json, arr_season)
#     #Convertir los pascales a hectopascales
#     data_json['pressure']= float(data_json['pressure'])*0.01 if (data_json['pressure']!="Nan") else "Nan"
#     data_json['spl'] = None if (data_json['spl']<=0) else data_json['spl']
#     data_json = roundUpThree(data_json)
#     return data_json


def gasConversionPPBtoMG(data_json, season):
    data_json = exceptions.checkVariable_helper(data_json, dict)
    season = exceptions.checkVariable_helper(season, list)

    data = {
        "ID": data_json["ID"],
        "CO": data_json["CO"],
        "CO_ug_m3": None,
        "H2S": data_json["H2S"],
        "H2S_ug_m3": None,
        "NO2": data_json["NO2"],
        "NO2_ug_m3": None,
        "O3": data_json["O3"],
        "O3_ug_m3": None,
        "PM1": data_json["PM1"],
        "PM10": data_json["PM10"],
        "PM25": data_json["PM25"],
        "SO2": data_json["SO2"],
        "SO2_ug_m3": None,
        "spl": data_json["spl"],
        "UV": data_json["UV"],
        "UVA": data_json["UVA"],
        "UVB": data_json["UVB"],
        "humidity": data_json["humidity"],
        "lat": data_json["lat"],
        "lon": data_json["lon"],
        "pressure": data_json["pressure"],
        "temperature": data_json["temperature"],
        "timestamp": data_json["timestamp"],
        "timestamp_zone": data_json["timestamp_zone"],
        "VOC": data_json["VOC"] if ("VOC" in data_json) else None,
        "CO2": data_json["CO2"] if ("CO2" in data_json) else None,
        "I_temperature": data_json["I_temperature"]
        if ("I_temperature" in data_json)
        else None,
    }

    for key in data:
        if key in pollutant:
            if (type(data[key]) is float) or (type(data[key]) is int):
                if key == "SO2":
                    data["SO2_ug_m3"] = data[key] * season[0]
                elif key == "NO2":
                    data["NO2_ug_m3"] = data[key] * season[1]
                elif key == "O3":
                    data["O3_ug_m3"] = data[key] * season[2]
                elif key == "CO":
                    data["CO_ug_m3"] = data[key] * season[3]
                elif key == "H2S":
                    data["H2S_ug_m3"] = data[key] * season[4]
    return data


def roundUpThree(data_json):
    data_json = exceptions.checkVariable_helper(data_json, dict)
    for i in range(len(array_ug_m3)):
        if (type(data_json[array_ug_m3[i]]) is float) or (
            type(data_json[array_ug_m3[i]]) is int
        ):
            data_json[array_ug_m3[i]] = round(data_json[array_ug_m3[i]], 3)
    return data_json


def checkNumberValues(data_json):
    """Helper Processed Measurement function to check number values"""
    data_json = exceptions.checkVariable_helper(data_json, dict)
    for i in range(len(array_ppb)):
        if data_json[array_ppb[i]] == "Nan":
            data_json[array_ppb[i]] = 0
    return data_json


def areFieldsValid(data):
    data = exceptions.checkVariable_helper(data, dict)
    for i in range(len(array_installation)):
        if (
            data[array_installation[i]] == ""
            or data[array_installation[i]] == None
        ):
            return False
    return True


def getFormatData(gas_average_measurement):
    gas_average_measurement_list = []
    if gas_average_measurement is not None:
        data = exceptions.checkVariable_helper(gas_average_measurement, list)
        next_hour = -1
        for measurement in gas_average_measurement:
            gas_measurement = measurement._asdict()
            hour = gas_measurement["timestamp_zone"].hour
            if next_hour == -1:
                gas_average_measurement_list.append(gas_measurement)
                next_hour = hour + 1
            else:
                if hour == next_hour:
                    gas_average_measurement_list.append(gas_measurement)
                else:
                    if (
                        next_hour > hour
                    ):  # si next_hour > hour => se resta con 24 horas
                        diff_0 = abs(24 - next_hour)
                        diff = diff_0 + hour
                    else:
                        diff = abs(hour - next_hour - 1)
                    for i in range(1, diff + 1):
                        new_variable = {
                            "timestamp_zone": before_date
                            + datetime.timedelta(hours=i),
                            "sensor": "",
                        }
                        gas_average_measurement_list.append(new_variable)
                    gas_average_measurement_list.append(gas_measurement)
                next_hour = hour + 1
            before_date = gas_measurement["timestamp_zone"]
            if next_hour == 24:
                next_hour = 0
        return gas_average_measurement_list
    return None


def setNoneStringElements(data_json):
    string_fields = ["ID", "timestamp_zone", "timestamp", "zone"]
    data_json = exceptions.checkVariable_helper(data_json, dict)
    for key in data_json:
        if (type(data_json[key]) is str) and (key not in string_fields):
            data_json[key] = None
    return data_json


def beautyFormatDate(date):
    return (
        addZero(date.day)
        + "-"
        + addZero(date.month)
        + "-"
        + addZero(date.year)
        + " "
        + addZero(date.hour)
        + ":"
        + addZero(date.minute)
        + ":"
        + addZero(date.second)
    )


def addZero(number):
    number = exceptions.checkVariable_helper(number, int)
    return "0" + str(number) if (number < 10) else str(number)


def checkValidLatLonValues(data_json):
    if (
        data_json["lat"] >= lat_lima_interval[0]
        and data_json["lat"] <= lat_lima_interval[1]
        and data_json["lon"] >= lon_lima_interval[0]
        and data_json["lon"] <= lon_lima_interval[1]
    ):
        return True
    return False


def getColorBaseOnGasValuesMobile(qhawax_inca):
    if isinstance(qhawax_inca, float) is not True:
        raise TypeError(
            "qHAWAX Inca value " + str(qhawax_inca) + " should be float"
        )

    return_color = "green"
    if qhawax_inca == 50:
        return_color = "green"
    elif qhawax_inca == 100:
        return_color = "yellow"
    elif qhawax_inca == 500:
        return_color = "orange"
    elif qhawax_inca == 600:
        return_color = "red"
    return return_color


def validaPollutant(val, sensor_name):
    calificacionInca = 0
    if sensor_name == "O3":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 175:
            calificacionInca = 500
        elif val > 175:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "SO2":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 625:
            calificacionInca = 500
        elif val > 625:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "CO":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 150:
            calificacionInca = 500
        elif val > 150:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "H2S":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 1000:
            calificacionInca = 500
        elif val > 1000:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "NO2":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 150:
            calificacionInca = 500
        elif val > 150:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "PM10":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 167:
            calificacionInca = 500
        elif val > 167:
            calificacionInca = 600
        else:
            calificacionInca = -1
    elif sensor_name == "PM25":
        if val >= 0 and val <= 50:
            calificacionInca = 50
        elif val > 50 and val <= 100:
            calificacionInca = 100
        elif val > 100 and val <= 500:
            calificacionInca = 500
        elif val > 500:
            calificacionInca = 600
        else:
            calificacionInca = -1
    else:
        calificacionInca = -1
    return calificacionInca


def getStartAndFinishTimestampBasedOnTurnAndTimestampMobile(timestamp, turn):
    date_conc = timestamp.strftime("%Y-%m-%d")
    if turn == 1:  # UTC
        time_start = "13:00:00"
        time_finish = "15:00:00"
    elif turn == 2:
        time_start = "15:00:00"
        time_finish = "17:00:00"
    elif turn == 3:
        time_start = "19:00:00"
        time_finish = "21:00:00"
    elif turn == 4:
        time_start = "21:00:00"
        time_finish = "23:00:00"
    start_time_reconstructed = dateutil.parser.parse(
        date_conc + " " + time_start
    )
    finish_time_reconstructed = dateutil.parser.parse(
        date_conc + " " + time_finish
    )
    return start_time_reconstructed, finish_time_reconstructed
