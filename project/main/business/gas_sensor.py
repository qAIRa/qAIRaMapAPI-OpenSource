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
        offsets = get_business_helper.getConstantsFromProductID(qhawax_name,'offsets')
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
        controlled_offsets = get_business_helper.getConstantsFromProductID(qhawax_name,'controlled-offsets')
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
        non_controlled_offsets = get_business_helper.getConstantsFromProductID(qhawax_name,'non-controlled-offsets')
        if(non_controlled_offsets is not None):
            return make_response(jsonify(non_controlled_offsets), 200)
        return make_response(jsonify('Gas Sensor does not exist due to qHAWAX '+str(qhawax_name)+' does not exist'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/save_gas_sensor_json/', methods=['POST'])
def saveGasSensorJson():
    req_json = request.get_json()
    try:
        qH_name, gas_sensor_json, description, in_charge = exception_helper.getGasSensorTargetofJson(req_json)
        post_business_helper.updateJsonGasSensor(qH_name, gas_sensor_json)
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': ' \'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Gas Sensor variables have been updated'}, 200)

