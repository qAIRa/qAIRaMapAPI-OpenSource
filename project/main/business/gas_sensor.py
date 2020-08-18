from flask import jsonify, make_response, request
from project.database.models import Qhawax, GasSensor
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/request_offsets/', methods=['GET'])
def requestOffsets():
    """
    endpoint to list offsets variable filter by qHAWAX ID

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        offsets = get_business_helper.getOffsetsFromProductID(qhawax_name)
        return make_response(jsonify(offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_controlled_offsets/', methods=['GET'])
def requestControlledOffsets():
    """
    endpoint to list controlled offsets variable filter by qHAWAX ID

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        controlled_offsets = get_business_helper.getControlledOffsetsFromProductID(qhawax_name)
        return make_response(jsonify(controlled_offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_non_controlled_offsets/', methods=['GET'])
def requestNonControlledOffsets():
    """
    endpoint to list non-controlled offsets variable filter by qHAWAX ID

    :type ID: string
    :param ID: qHAWAX Name

    """
    qhawax_name = request.args.get('ID')
    try:
        non_controlled_offsets = get_business_helper.getNonControlledOffsetsFromProductID(qhawax_name)
        return make_response(jsonify(non_controlled_offsets), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/save_offsets/', methods=['POST'])
def saveOffsets():
    """
    endpoint to save offset variables

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type offsets: Json
    :param offsets: Json of offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['product_id']).strip()
        offsets = req_json['offsets']
        try:
            post_business_helper.updateOffsetsFromProductID(qhawax_name, offsets)
            description="Se actualizaron constantes offsets"
            observation_type="Interna"
            person_in_charge = req_json['person_in_charge']
            post_business_helper.writeBinnacle(qhawax_name,observation_type,description,person_in_charge)
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
    endpoint to save controlled offset variables

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type controlled_offsets: Json
    :param controlled_offsets: Json of controlled offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['product_id']).strip()
        controlled_offsets = req_json['controlled_offsets']
    except KeyError as e:
        json_message = jsonify({'error': 'Parameter \'%s\' is missing in JSON object' % (e)})
        return make_response(json_message, 400)

    post_business_helper.updateControlledOffsetsFromProductID(qhawax_name, controlled_offsets)
    description="Se actualizaron constantes controladas"
    observation_type="Interna"
    person_in_charge = req_json['person_in_charge']
    post_business_helper.writeBinnacle(qhawax_name,observation_type,description,person_in_charge)
    return make_response('Success', 200)

@app.route('/api/save_non_controlled_offsets/', methods=['POST'])
def saveNonControlledOffsets():
    """
    endpoint to save non controlled offset variables

    :type product_id: integer
    :param product_id: qHAWAX Name

    :type non_controlled_offsets: Json
    :param non_controlled_offsets: Json of non controlled offset variable of qHAWAX

    """
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['product_id']).strip()
        non_controlled_offsets = req_json['non_controlled_offsets']
    except KeyError as e:
        json_message = jsonify({'error': 'Parameter \'%s\' is missing in JSON object' % (e)})
        return make_response(json_message, 400)

    post_business_helper.updateNonControlledOffsetsFromProductID(qhawax_name, non_controlled_offsets)
    description="Se actualizaron constantes no controladas"
    observation_type="Interna"
    person_in_charge = req_json['person_in_charge']
    post_business_helper.writeBinnacle(qhawax_name,observation_type,description,person_in_charge)
    return make_response('Success', 200)

