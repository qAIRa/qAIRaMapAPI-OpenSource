from flask import jsonify, make_response, request
import datetime
from datetime import timedelta
import json
import pytz
import dateutil.parser
import dateutil.tz
from project import app, db, socketio
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.util_helper as util_helper
import project.main.same_function_helper as same_helper

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
        if processed_measurements is not []:
            processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
            return make_response(jsonify(processed_measurements_list), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/dataProcessed/', methods=['POST'])
def handleProcessedData():
    """
    To record processed measurement and valid processed measurement every five seconds  

    """
    try:
        flag_email = False
        data_json = request.get_json()
        product_id = data_json['ID']
        data_json = util_helper.validTimeJsonProcessed(data_json)
        data_json = util_helper.validAndBeautyJsonProcessed(data_json)
        helper.storeProcessedDataInDB(data_json)
        data_json['ID'] = product_id
        data_json['zone'] = "Zona No Definida"
        qhawax_id = helper.getQhawaxId(product_id)
        mode = helper.getQhawaxMode(qhawax_id)
        if(mode == "Cliente"):
            qhawax_zone = get_data_helper.getNoiseData(product_id)
            data_json['zone'] = qhawax_zone
            minutes_difference,last_time_turn_on = get_data_helper.getHoursDifference(qhawax_id)
            if(minutes_difference!=None):
                if(minutes_difference<5):
                    if(last_time_turn_on + datetime.timedelta(minutes=10) < datetime.datetime.now(dateutil.tz.tzutc())):
                        post_data_helper.storeValidProcessedDataInDB(data_json,qhawax_id)
                        socketio.emit('new_data_summary_valid', data_json) 
                elif(minutes_difference>=5):
                    if(last_time_turn_on + datetime.timedelta(hours=2) < datetime.datetime.now(dateutil.tz.tzutc())):
                        post_data_helper.storeValidProcessedDataInDB(data_json,qhawax_id)
                        socketio.emit('new_data_summary_valid', data_json) 
        socketio.emit('new_data_summary_processed', data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/processed_measurements_period/', methods=['GET'])
def getProcessedMeasurementsTimePeriod():
    """
    To list all measurement of processed measurement table in a define period of time

    :type name: string
    :param name: qHAWAX name

    :type initial_timestamp: timestamp without timezone
    :param initial_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    :type final_timestamp: timestamp without timezone
    :param final_timestamp: timestamp day-month-year hour:minute:second (UTC OO)

    """
    try:
        qhawax_name = request.args.get('name')
        #Recibiendo las horas indicadas a formato UTC 00:00
        initial_timestamp = request.args.get('initial_timestamp')
        final_timestamp = request.args.get('final_timestamp')
        date_format = '%d-%m-%Y %H:%M:%S'
        processed_measurements = get_data_helper.queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp,date_format)
        if processed_measurements is not None:
            processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
            return make_response(jsonify(processed_measurements_list), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


