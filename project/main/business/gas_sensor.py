from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import Qhawax, GasSensor
import project.main.business.business_helper as helper
from sqlalchemy import or_

@app.route('/api/request_offsets/', methods=['GET'])
def requestOffsets():
    """
    get qHAWAX offsets

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        offsets = helper.getOffsetsFromProductID(qhawax_name)
        return make_response(jsonify(offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_controlled_offsets/', methods=['GET'])
def requestControlledOffsets():
    """
    get qHAWAX controlled offsets

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        controlled_offsets = helper.getControlledOffsetsFromProductID(qhawax_name)
        return make_response(jsonify(controlled_offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_non_controlled_offsets/', methods=['GET'])
def requestNonControlledOffsets():
    """
    get qHAWAX non controlled offsets

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        non_controlled_offsets = helper.getNonControlledOffsetsFromProductID(qhawax_name)
        print(non_controlled_offsets)
        return make_response(jsonify(non_controlled_offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/save_offsets/', methods=['POST'])
def saveOffsets():
    """
    save qHAWAX offsets

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type offsets: Json
    :param offsets: Json of offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_id = str(req_json['product_id']).strip()
        offsets = req_json['offsets']
        try:
            helper.updateOffsetsFromProductID(qhawax_id, offsets)
            description="Se actualizaron constantes offsets"
            observation_type="Interna"
            solution = None
            person_in_charge = req_json['person_in_charge']
            end_date = None
            helper.writeBitacora(qhawax_id,observation_type,description,solution,person_in_charge,end_date)
            return make_response('Success', 200)
        except TypeError as e:
            json_message = jsonify({'error': '\'%s\'' % (e)})
            return make_response(json_message, 400)
    except KeyError as e:
        json_message = jsonify({'error': 'Parameter \'%s\' is missing in JSON object' % (e)})
        return make_response(json_message, 400)
    
    
    

@app.route('/api/save_controlled_offsets/', methods=['POST'])
def saveControlledOffsets():
    """
    save qHAWAX controlled offsets

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type controlled_offsets: Json
    :param controlled_offsets: Json of controlled offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_id = str(req_json['product_id']).strip()
        controlled_offsets = req_json['controlled_offsets']
    except KeyError as e:
        json_message = jsonify({'error': 'Parameter \'%s\' is missing in JSON object' % (e)})
        return make_response(json_message, 400)

    helper.updateControlledOffsetsFromProductID(qhawax_id, controlled_offsets)
    description="Se actualizaron constantes controladas"
    observation_type="Interna"
    solution = None
    person_in_charge = req_json['person_in_charge']
    end_date = None
    helper.writeBitacora(qhawax_id,observation_type,description,solution,person_in_charge,end_date)
    return make_response('Success', 200)

@app.route('/api/save_non_controlled_offsets/', methods=['POST'])
def saveNonControlledOffsets():
    """
    save qHAWAX non controlled offsets

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type non_controlled_offsets: Json
    :param non_controlled_offsets: Json of non controlled offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_id = str(req_json['product_id']).strip()
        non_controlled_offsets = req_json['non_controlled_offsets']
    except KeyError as e:
        json_message = jsonify({'error': 'Parameter \'%s\' is missing in JSON object' % (e)})
        return make_response(json_message, 400)

    helper.updateNonControlledOffsetsFromProductID(qhawax_id, non_controlled_offsets)
    description="Se actualizaron constantes no controladas"
    observation_type="Interna"
    solution = None
    person_in_charge = req_json['person_in_charge']
    end_date = None
    helper.writeBitacora(qhawax_id,observation_type,description,solution,person_in_charge,end_date)
    return make_response('Success', 200)

@app.route('/api/measurementPromedio/', methods=['GET'])
def requestProm():
    """
    get average of determine pollutant (CO,H2S,NO2,O3,PM10,PM25,SO2)

    :type name: string
    :param name: qHAWAX Name

    :type sensor: string
    :param sensor: qHAWAX pollutant

    :type hoursSensor: number
    :param hoursSensor: quantity of hours to get average

    :type minutes_diff: number
    :param minutes_diff: quantity of minutes after qHAWAX ON

    :type last_time_turn_on: timestamp without timezone
    :param last_time_turn_on: time of qHAWAX ON

    """
    name = request.args.get('name')
    sensor = request.args.get('sensor')
    hoursSensor = request.args.get('hoursSensor')
    minutes_diff = int(request.args.get('minutes_diff'))  
    if(minutes_diff<5):
        last_time_turn_on = dateutil.parser.parse(request.args.get('last_time_turn_on')) + datetime.timedelta(minutes=10)
    elif(minutes_diff>=5):
        last_time_turn_on = dateutil.parser.parse(request.args.get('last_time_turn_on')) + datetime.timedelta(hours=2)
    final_timestamp = datetime.datetime.now() - datetime.timedelta(hours=5)
    initial_timestamp = final_timestamp - datetime.timedelta(hours=int(hoursSensor))
    if(initial_timestamp.replace(tzinfo=None)>=last_time_turn_on.replace(tzinfo=None)):
        qhawax_measurement_sensor = helper.queryDBPROM(name, sensor, initial_timestamp, final_timestamp)
    else:
        qhawax_measurement_sensor=-1
    return str(qhawax_measurement_sensor)

