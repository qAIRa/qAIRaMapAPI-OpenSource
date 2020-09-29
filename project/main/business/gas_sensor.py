from flask import jsonify, make_response, request
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/request_gas_sensor_variables/', methods=['GET'])
def requestGasSensorVariable():
    qhawax_name = request.args.get('ID')
    variable_type = str(request.args.get('gas_sensor_type'))
    variable_gas_sensor = None
    try:
        if(variable_type=='offset'):
            variable_gas_sensor = get_business_helper.getOffsetsFromProductID(qhawax_name)
        elif(variable_type=='controlled-offset'):
            variable_gas_sensor = get_business_helper.getControlledOffsetsFromProductID(qhawax_name)
        elif(variable_type=='non-controlled-offset'):
            variable_gas_sensor = get_business_helper.getNonControlledOffsetsFromProductID(qhawax_name)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        print(variable_gas_sensor)
        if(variable_gas_sensor is not None):
            return make_response(jsonify(variable_gas_sensor), 200)
        return make_response(jsonify({'Warning':'qHAWAX name has not been found'}), 200)

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

