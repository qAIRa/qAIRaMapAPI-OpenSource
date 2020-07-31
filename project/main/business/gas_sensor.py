from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz

from project import app, db, socketio
from project.database.models import Qhawax, GasSensor
import project.main.business.business_helper as helper

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
            person_in_charge = req_json['person_in_charge']
            helper.writeBitacora(qhawax_id,observation_type,description,person_in_charge)
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
    person_in_charge = req_json['person_in_charge']
    helper.writeBitacora(qhawax_id,observation_type,description,person_in_charge)
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
    person_in_charge = req_json['person_in_charge']
    helper.writeBitacora(qhawax_id,observation_type,description,person_in_charge)
    return make_response('Success', 200)

