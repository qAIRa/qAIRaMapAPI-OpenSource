from flask import jsonify, make_response, request
from flask_socketio import join_room
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import Qhawax, ProcessedMeasurement, AirQualityMeasurement
import project.main.data.data_helper as helper
from sqlalchemy import or_


@app.route('/api/air_quality_measurements/', methods=['GET', 'POST'])
def storeAirQualityData():
    if request.method == 'GET':
        qhawax_name = request.args.get('name')
        interval_hours = int(request.args.get('interval_hours')) \
            if request.args.get('interval_hours') is not None else 1
        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc()) - datetime.timedelta(hours=5)
        initial_timestamp = final_timestamp - datetime.timedelta(hours=interval_hours)
        air_quality_measurements = helper.queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp)

        if air_quality_measurements is not None:
            air_quality_measurements_list = [measurement._asdict() for measurement in air_quality_measurements]
            return make_response(jsonify(air_quality_measurements_list), 200)
        else:
            return make_response(jsonify('Measurements not found'), 404)

    if request.method == 'POST':
        try:
            data_json = request.get_json()
            helper.storeAirQualityDataInDB(data_json)
            return make_response('OK', 200)
        except Exception as e:
            print(e)
            return make_response('Invalid format. Exception="%s"' % (e), 400)

@app.route('/api/air_quality_measurements_period/', methods=['GET'])
def getAirQualityMeasurementsTimePeriod():
    qhawax_name = request.args.get('name')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    air_quality_measurements = helper.queryDBAirQuality(qhawax_name, initial_timestamp, final_timestamp)

    if air_quality_measurements is not None:
        air_quality_measurements_list = [measurement._asdict() for measurement in air_quality_measurements]
        return make_response(jsonify(air_quality_measurements_list), 200)
    else:
        return make_response(jsonify('Measurements not found'), 404)

@app.route('/api/gas_average_measurement/', methods=['GET'])
def getGasAverageMeasurementsEvery24():
    qhawax_name = request.args.get('qhawax')
    gas_name = request.args.get('gas')
    installation_id = helper.getInstallationIdBaseName(qhawax_name)
    values = helper.getTimeQhawaxHistory(installation_id)
    values_list = {'last_time_on': values[0], 'last_time_registration': values[1]} 
    gas_average_measurement = helper.queryDBGasAverageMeasurement(qhawax_name, gas_name,values_list)
    gas_average_measurement_list = []
    if gas_average_measurement is not None:
        next_hour = -1
        for measurement in gas_average_measurement:
            gas_measurement = measurement._asdict() 
            hour = gas_measurement["timestamp"].hour

            if(next_hour == -1): 
                gas_average_measurement_list.append(gas_measurement)
                next_hour = hour + 1
            else:
                if(hour == next_hour): 
                    gas_average_measurement_list.append(gas_measurement)
                    last_date = gas_measurement["timestamp"]
                else:
                    diff = hour - next_hour
                    for i in range(1,diff+2):
                        new_variable ={"timestamp":last_date + datetime.timedelta(hours=i),"sensor":""}
                        gas_average_measurement_list.append(new_variable)
                next_hour = hour + 1

            if(next_hour == 24): next_hour = 0

        return make_response(jsonify(gas_average_measurement_list), 200)
    else:
        return make_response(jsonify('Measurements not found'), 404)

@app.route('/api/average_valid_processed_period/', methods=['GET'])
def getAverageValidProcessedMeasurementsTimePeriodByCompany():
    qhawax_id = request.args.get('qhawax_id')
    company_id = request.args.get('company_id')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    average_valid_processed_measurements=[]
    if(int(company_id)!=1):
        if (helper.qhawaxBelongsCompany(qhawax_id,company_id)):   
            average_valid_processed_measurements = helper.queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp)
    elif (int(company_id)==1):
        average_valid_processed_measurements = helper.queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp)
    
    average_valid_processed_measurements_list = []

    if average_valid_processed_measurements is not None:
        for valid_measurement in average_valid_processed_measurements:
            valid_measurement = valid_measurement._asdict() 
            dict_valid={'CO_ug_m3': valid_measurement['CO_ug_m3'], 'H2S_ug_m3': valid_measurement['H2S_ug_m3'],'NO2_ug_m3': valid_measurement['NO2_ug_m3'],'O3_ug_m3': valid_measurement['O3_ug_m3'],'PM10': valid_measurement['PM10'],
                'PM25': valid_measurement['PM25'],'SO2_ug_m3': valid_measurement['SO2_ug_m3'],'SPL': valid_measurement['spl'],'UV': valid_measurement['uv'],
                'humidity': valid_measurement['humidity'],'lat':valid_measurement['lat'],'lon':valid_measurement['lon'],
                'pressure': valid_measurement['pressure'],'temperature': valid_measurement['temperature'],'timestamp': valid_measurement['timestamp']}
            average_valid_processed_measurements_list.append(dict_valid)
        return make_response(jsonify(average_valid_processed_measurements_list), 200)
    return make_response(jsonify('Valid Measurements not found'), 404)