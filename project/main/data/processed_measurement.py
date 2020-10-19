from flask import jsonify, make_response, request
import datetime
from datetime import timedelta
import dateutil.parser
import dateutil.tz
from project import app, db, socketio
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper
import project.main.business.get_business_helper as get_business_helper

@app.route('/api/processed_measurements/', methods=['GET'])
def getProcessedData():
    """
    To list all measurement of processed measurement table record the last N minutes
    """
    try:
        qhawax_name = request.args.get('name')
        interval_minutes = int(request.args.get('interval_minutes')) \
            if request.args.get('interval_minutes') is not None else 60 

        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
        initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes) 
        date_format = '%Y-%m-%d %H:%M:%S.%f%z'
        processed_measurements = get_data_helper.queryDBProcessed(qhawax_name, str(initial_timestamp), \
                                                                  str(final_timestamp),date_format)
        if processed_measurements is not None:
            return make_response(jsonify(processed_measurements), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/dataProcessed/', methods=['POST'])
def handleProcessedData():
    """ To record processed measurement and valid processed measurement every five seconds  """
    try:
        data_json = request.get_json()
        i_temperature = None
        if('I_temperature' in data_json):
            i_temperature = data_json['I_temperature']
        product_id = data_json['ID']
        data_json = util_helper.validTimeJsonProcessed(data_json)
        data_json = util_helper.validAndBeautyJsonProcessed(data_json)
        post_data_helper.storeProcessedDataInDB(data_json)
        data_json['ID'] = product_id
        data_json['zone'] = "Zona No Definida"
        qhawax_id = same_helper.getQhawaxID(product_id)
        mode = same_helper.getQhawaxMode(product_id)
        if(mode == "Cliente"):
            qhawax_zone = get_data_helper.getNoiseData(product_id)
            data_json['zone'] = qhawax_zone
            minutes_difference,last_time_turn_on = get_data_helper.getHoursDifference(qhawax_id)
            if(minutes_difference!=None):
                if(minutes_difference<5):
                    if(last_time_turn_on + datetime.timedelta(minutes=10) < datetime.datetime.now(dateutil.tz.tzutc())):
                        post_data_helper.storeValidProcessedDataInDB(data_json,qhawax_id)
                elif(minutes_difference>=5):
                    if(last_time_turn_on + datetime.timedelta(hours=2) < datetime.datetime.now(dateutil.tz.tzutc())):
                        post_data_helper.storeValidProcessedDataInDB(data_json,qhawax_id)
        data_json = util_helper.NanToCeroJsonProcessed(data_json,i_temperature)
        socketio.emit('new_data_summary_processed', data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/processed_measurements_period/', methods=['GET'])
def getProcessedMeasurementsTimePeriod():
    """
    To list all measurement of processed measurement table in a define period of time

    """
    try:
        qhawax_name = request.args.get('name')
        initial_timestamp = request.args.get('initial_timestamp')
        final_timestamp = request.args.get('final_timestamp')
        date_format = '%d-%m-%Y %H:%M:%S'
        processed_measurements = get_data_helper.queryDBProcessed(qhawax_name, \
                                                 initial_timestamp, final_timestamp,date_format)
        if processed_measurements is not None:
            return make_response(jsonify(processed_measurements), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/get_time_processed_data_active_qhawax/', methods=['GET'])
def getQhawaxProcessedLatestTimestamp():
    """
    To get qHAWAX Processed Measurement latest timestamp

    """
    try:
        qhawax_name = request.args.get('qhawax_name')
        processed_timestamp = get_business_helper.getLatestTimeInProcessedMeasurement(qhawax_name)
        if(processed_timestamp is not None):
            if(processed_timestamp is ""):
                return make_response({'Warning':' qHAWAX name has not been found in Processed Measurement'},200)
            return make_response(str(processed_timestamp),200)
        return make_response({'Warning': 'qHAWAX name has not been found qHAWAX table'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

