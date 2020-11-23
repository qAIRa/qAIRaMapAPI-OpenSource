from flask import jsonify, make_response, request
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/request_offsets/', methods=['GET'])
def requestOffsets():
    """ get qHAWAX offsets"""
    qhawax_name = request.args.get('ID')
    try:
        offsets = get_business_helper.getOffsetsFromProductID(qhawax_name)
        if(offsets is not None):
            return make_response(jsonify(offsets), 200)
        return make_response(jsonify('Gas Sensor does not exist due to qHAWAX '+str(qhawax_name)+' does not exist'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_controlled_offsets/', methods=['GET'])
def requestControlledOffsets():
    """ get qHAWAX controlled offsets """
    qhawax_name = request.args.get('ID')
    try:
        controlled_offsets = get_business_helper.getControlledOffsetsFromProductID(qhawax_name)
        if(controlled_offsets is not None):
            return make_response(jsonify(controlled_offsets), 200)
        return make_response(jsonify('Gas Sensor does not exist due to qHAWAX '+str(qhawax_name)+' does not exist'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/request_non_controlled_offsets/', methods=['GET'])
def requestNonControlledOffsets():
    """ get qHAWAX non controlled offsets"""
    qhawax_name = request.args.get('ID')
    try:
        non_controlled_offsets = get_business_helper.getNonControlledOffsetsFromProductID(qhawax_name)
        if(non_controlled_offsets is not None):
            return make_response(jsonify(non_controlled_offsets), 200)
        return make_response(jsonify('Gas Sensor does not exist due to qHAWAX '+str(qhawax_name)+' does not exist'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/save_gas_sensor_json/', methods=['POST'])
def saveGasSensorJson():
    try:
        req_json = request.get_json()
        exception_helper.getGasSensorTargetofJson(req_json)
        qhawax_name = str(req_json['product_id']).strip()
        gas_sensor_json = req_json['gas_sensor_json']
        description =req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.updateJsonGasSensor(qhawax_name, gas_sensor_json)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': ' \'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Gas Sensor variables have been updated'}, 200)

