from flask import jsonify, make_response, request
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
    """
    GET: To list all measurement in ppb of air quality measurement table
    This is an hourly average measurement

    :type name: string
    :param name: qHAWAX name

    :type interval_hours: integer
    :param interval_hours: the last N hours we want it 

    POST: To record processed measurement and valid processed measurement every five seconds
    
    Json input of Air Quality Measurement

    """
    if request.method == 'GET':
        qhawax_name = request.args.get('name')
        interval_hours = int(request.args.get('interval_hours')) \
            if request.args.get('interval_hours') is not None else 1
        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
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
            print("Entre a air_quality_measurements y todo bien")
            print(data_json)
            helper.storeAirQualityDataInDB(data_json)
            return make_response('OK', 200)
        except Exception as e:
            print(e)
            return make_response('Invalid format. Exception="%s"' % (e), 400)

@app.route('/api/air_quality_measurements_period/', methods=['GET'])
def getAirQualityMeasurementsTimePeriod():
    """
    To list all measurement in ppb of air quality measurement table in a define period of time
    This is an hourly average measurement

    :type name: string
    :param name: qHAWAX name

    :type initial_timestamp: timestamp without timezone
    :param initial_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    :type final_timestamp: timestamp without timezone
    :param final_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    """
    qhawax_name = request.args.get('name')
    initial_timestamp_utc = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
    final_timestamp_utc = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')
    air_quality_measurements = helper.queryDBAirQuality(qhawax_name, initial_timestamp_utc, final_timestamp_utc)

    if air_quality_measurements is not None:
        air_quality_measurements_list = [measurement._asdict() for measurement in air_quality_measurements]
        return make_response(jsonify(air_quality_measurements_list), 200)
    else:
        return make_response(jsonify('Measurements not found'), 404)

@app.route('/api/gas_average_measurement/', methods=['GET'])
def getGasAverageMeasurementsEvery24():
    """
    To list all values by a define gas or dust in ug/m3 of air quality measurement table of the last 24 hours

    :type qhawax: string
    :param qhawax: qHAWAX name

    :type gas: string
    :param gas: gas or dust name (CO,H2S,O3,NO2,SO2,PM25,PM10)

    """
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
                last_date = gas_measurement["timestamp"]
                if(hour == next_hour): 
                    gas_average_measurement_list.append(gas_measurement)                   
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
    """
    To list all average measurement of valid processed measurement table in a define period of time and company

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type company_id: integer
    :param company_id: company ID

    :type initial_timestamp: timestamp without timezone
    :param initial_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    :type final_timestamp: timestamp without timezone
    :param final_timestamp: timestamp day-month-year hour:minute:second (UTC OO)
    """
    qhawax_id = request.args.get('qhawax_id')
    company_id = request.args.get('company_id')
    initial_timestamp = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
    final_timestamp = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')

    average_valid_processed_measurements=[]
    if(int(company_id)!=1):
        if (helper.qhawaxBelongsCompany(qhawax_id,company_id)):   
            average_valid_processed_measurements = helper.queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp)
    elif (int(company_id)==1):
        average_valid_processed_measurements = helper.queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp)
    
    average_valid_processed_measurements_list = []

    if average_valid_processed_measurements is not None:
        average_valid_processed_measurements_list = [measurement._asdict() for measurement in average_valid_processed_measurements]
        return make_response(jsonify(average_valid_processed_measurements_list), 200)
    return make_response(jsonify('Valid Measurements not found'), 404)