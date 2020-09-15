from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
from project import app, db
import project.main.data.get_data_helper as get_data_helper
import project.main.same_function_helper as same_helper

@app.route('/api/valid_processed_measurements_period/', methods=['GET'])
def getValidProcessedMeasurementsTimePeriod():
    """
    To list all measurement of valid processed measurement table in a define period of time and company

    """
    qhawax_id = int(request.args.get('qhawax_id'))\
                if request.args.get('qhawax_id') is not None else 0
    initial_timestamp = str(request.args.get('initial_timestamp'))\
                        if request.args.get('initial_timestamp') is not None else "01-01-2020 00:00:00"
    final_timestamp = str(request.args.get('final_timestamp'))\
                      if request.args.get('final_timestamp') is not None else "01-01-2020 01:00:00"
    try:
        date_format = '%d-%m-%Y %H:%M:%S'
        valid_processed_measurements = get_data_helper.queryDBValidProcessedByQhawaxScript(qhawax_id,\
                                                                        initial_timestamp, final_timestamp,\
                                                                        date_format)
        if valid_processed_measurements is not None:
            return make_response(jsonify(valid_processed_measurements), 200)
        return make_response(jsonify('Valid Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/valid_processed_measurements/', methods=['GET'])
def getValidProcessedData():
    """
    To list all measurement of valid processed measurement table record the last N minutes

    """
    qhawax_name = request.args.get('name') \
                  if request.args.get('name') is not None else ""
    interval_minutes = int(request.args.get('interval_minutes')) \
                       if request.args.get('interval_minutes') is not None else 60
    try:
        qhawax_id = same_helper.getQhawaxID(qhawax_name)
        if(qhawax_id is not None):
            final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
            initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes)
            date_format = '%Y-%m-%d %H:%M:%S.%f%z'
            valid_processed_measurements = get_data_helper.queryDBValidProcessedByQhawaxScript(qhawax_id, \
                                                                str(initial_timestamp), str(final_timestamp),\
                                                                date_format)
            if valid_processed_measurements is not None:
                return make_response(jsonify(valid_processed_measurements), 200)
            return make_response(jsonify('Valid Measurements not found'), 200)
        return make_response(jsonify('qHAWAX ID does not exist'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_time_valid_data_active_qhawax/', methods=['GET'])
def getTimeOfValidProcessed():
    """
    Get the time of the last record in valid processed measurement table
    If this qHAWAX does not exist, return []

    """
    qhawax_name = request.args.get('name')\
                  if request.args.get('name') is not None else ""
    try:
        if(get_data_helper.getLatestTimestampValidProcessed(qhawax_name) is not None):
            return str(get_data_helper.getLatestTimestampValidProcessed(qhawax_name))
        return make_response(jsonify('qHAWAX name does not exist in field'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/daily_valid_processed_measurements/', methods=['GET'])
def getDailyValidProcessedData():
    """
    To list all measurement of valid processed measurement table in a define period of time
    """
    qhawax_id = int(request.args.get('id')) \
                if request.args.get('id') is not None else 0
    initial_timestamp_utc = str(request.args.get('start_date'))\
                            if request.args.get('start_date') is not None else "2020-01-01 00:00:00"
    final_timestamp_utc = str(request.args.get('end_date'))\
                          if request.args.get('end_date') is not None else "2020-01-01 01:00:00"
    try:
        installation_id = same_helper.getInstallationId(qhawax_id)
        if(installation_id is not None):
            date_format = '%Y-%m-%d %H:%M:%S'
            valid_processed_measurements = get_data_helper.queryDBDailyValidProcessedByQhawaxScript(installation_id, \
                                                                            initial_timestamp_utc, final_timestamp_utc,\
                                                                            date_format)
            if valid_processed_measurements is not None:
                return make_response(jsonify(valid_processed_measurements), 200)
            return make_response(jsonify('Daily Valid Measurements not found'), 200)
        return make_response(jsonify('qHAWAX ID does not exist in field'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
