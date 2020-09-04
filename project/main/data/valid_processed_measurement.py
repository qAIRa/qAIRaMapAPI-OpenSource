from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
from project import app, db, socketio
from project.database.models import Qhawax
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

#@app.route('/api/valid_processed_measurements_period/', methods=['GET'])
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
    try:
        qhawax_id = int(request.args.get('qhawax_id'))
        initial_timestamp = request.args.get('initial_timestamp')
        final_timestamp = request.args.get('final_timestamp')

        valid_processed_measurements = get_data_helper.queryDBValidProcessedByQhawaxScript(qhawax_id,initial_timestamp, final_timestamp)
        if valid_processed_measurements is not None:
            valid_processed_measurements_list = [measurement._asdict() for measurement in valid_processed_measurements]
            return make_response(jsonify(valid_processed_measurements_list), 200)
        return make_response(jsonify('Valid Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


#@app.route('/api/valid_processed_measurements/', methods=['GET'])
def getValidProcessedData():
    """
    To list all measurement of valid processed measurement table record the last N minutes

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type interval_minutes: integer
    :param interval_minutes: the last N minutes we want it 

    """
    try:
        qhawax_name = request.args.get('name')
        interval_minutes = int(request.args.get('interval_minutes')) \
            if request.args.get('interval_minutes') is not None else 60
        
        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
        initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes)

        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        valid_processed_measurements={}
        
        valid_processed_measurements = get_data_helper.queryDBValidProcessedByQhawaxScript(qhawax_id, \
                                                                                  str(initial_timestamp), str(final_timestamp))
        if valid_processed_measurements is not None:
            valid_processed_measurements_list = [valid_measurement._asdict() for valid_measurement in valid_processed_measurements]
            return make_response(jsonify(valid_processed_measurements_list), 200)
        return make_response(jsonify('Valid Measurements not found'), 404)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/get_time_valid_data_active_qhawax/', methods=['GET'])
def getTimeOfValidProcessed():
    """
    Get the time of the last record in valid processed measurement table
    If this qHAWAX does not exist, return []

    :type name: string
    :param name: qHAWAX name

    """
    try:
        qhawax_name = request.args.get('name')
        return str(get_data_helper.getLatestTimestampValidProcessed(qhawax_name))
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

