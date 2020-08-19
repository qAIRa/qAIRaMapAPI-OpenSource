from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import Qhawax, ProcessedMeasurement
import project.main.data.data_helper as helper
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

@app.route('/api/valid_processed_measurements_period/', methods=['GET'])
def getValidProcessedMeasurementsTimePeriod():
    """
    To list all measurement of valid processed measurement table in a define period of time and company

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type initial_timestamp: timestamp without timezone
    :param initial_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    :type final_timestamp: timestamp without timezone
    :param final_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    """
    qhawax_id = int(request.args.get('qhawax_id'))
    initial_timestamp_utc = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
    final_timestamp_utc = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')

    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id!= None):
        valid_processed_measurements = helper.queryDBValidProcessedByQhawaxScript(installation_id, \
                                                                                initial_timestamp_utc, final_timestamp_utc)
        if valid_processed_measurements is not None:
            valid_processed_measurements_list = [measurement._asdict() for measurement in valid_processed_measurements]
            return make_response(jsonify(valid_processed_measurements_list), 200)
    else:
        return make_response(jsonify('Valid Measurements not found'), 200)
        
    return make_response(jsonify('Valid Measurements not found'), 404)

@app.route('/api/daily_valid_processed_measurements/', methods=['GET'])
def getDailyValidProcessedData():
    """
    To list all measurement of valid processed measurement table in a define period of time

    :type id: integer
    :param id: qHAWAX ID

    :type start_date: timestamp without timezone
    :param start_date: initial timestamp day-month-year hour:minute:second (UTC OO)

    :type end_date: timestamp without timezone
    :param end_date: final timestamp day-month-year hour:minute:second (UTC OO)
    

    """
    qhawax_id = int(request.args.get('qhawax_id'))
    initial_timestamp_utc = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%Y-%m-%d %H:%M:%S')
    final_timestamp_utc = datetime.datetime.strptime(request.args.get('final_timestamp'), '%Y-%m-%d %H:%M:%S')
    
    installation_id = same_helper.getInstallationId(qhawax_id)
    if(installation_id!= None):
        valid_processed_measurements = helper.queryDBValidProcessedByQhawaxScript(installation_id, initial_timestamp_utc, final_timestamp_utc)
        if valid_processed_measurements is not None:
            valid_processed_measurements_list = [daily_valid_measurement._asdict() for daily_valid_measurement in valid_processed_measurements]
            return make_response(jsonify(valid_processed_measurements_list), 200)
    else:
        return make_response(jsonify('Any Valid ProcessedMeasurement found'), 200)

    return make_response(jsonify('It was an error'), 404)

@app.route('/api/valid_processed_measurements/', methods=['GET'])
def getValidProcessedData():
    """
    To list all measurement of valid processed measurement table record the last N minutes

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type interval_minutes: integer
    :param interval_minutes: the last N minutes we want it 

    """
    qhawax_name = request.args.get('name')
    interval_minutes = int(request.args.get('interval_minutes')) \
        if request.args.get('interval_minutes') is not None else 60
    final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
    initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes)
    qhawax_id = db.session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    valid_processed_measurements={}
    
    if(qhawax_id!=None):
        installation_id = same_helper.getInstallationId(qhawax_id)
        valid_processed_measurements = helper.queryDBValidProcessedByQhawaxScript(installation_id, \
                                                                                  initial_timestamp, final_timestamp)

    if valid_processed_measurements is not None:
        valid_processed_measurements_list = [valid_measurement._asdict() for valid_measurement in valid_processed_measurements]
        return make_response(jsonify(valid_processed_measurements_list), 200)
    else:
        return make_response(jsonify('Valid Measurements not found'), 404)

@app.route('/api/get_time_valid_data_active_qhawax/', methods=['GET'])
def getTimeOfValidProcessed():
    """
    Get the time of the last record in valid processed measurement table
    If this qHAWAX does not exist, return []

    :type name: string
    :param name: qHAWAX name

    """
    qhawax_name = request.args.get('name')
    return str(helper.getLatestTimestampValidProcessed(qhawax_name))

