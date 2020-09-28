from flask import jsonify, make_response, request
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/request_offsets/', methods=['GET'])
def requestOffsets():
    qhawax_name = request.args.get('ID')
    try:
        offsets = get_business_helper.getOffsetsFromProductID(qhawax_name)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        if(offsets is not None):
            return make_response(jsonify(offsets), 200)
        return make_response(jsonify({'Warning':'qHAWAX name has not been found'}), 200)

@app.route('/api/request_controlled_offsets/', methods=['GET'])
def requestControlledOffsets():
    qhawax_name = request.args.get('ID')
    try:
        controlled_offsets = get_business_helper.getControlledOffsetsFromProductID(qhawax_name)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        if(controlled_offsets is not None):
            return make_response(jsonify(controlled_offsets), 200)
        return make_response(jsonify({'Warning':'qHAWAX name has not been found'}), 200)

@app.route('/api/request_non_controlled_offsets/', methods=['GET'])
def requestNonControlledOffsets():
    qhawax_name = request.args.get('ID')
    try:
        non_controlled_offsets = get_business_helper.getNonControlledOffsetsFromProductID(qhawax_name)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        if(non_controlled_offsets is not None):
            return make_response(jsonify(non_controlled_offsets), 200)
        return make_response(jsonify({'Warning':'qHAWAX name has not been found'}), 200)


@app.route('/api/save_offsets/', methods=['POST'])
def saveOffsets():
    try:
        req_json = request.get_json()
        exception_helper.getOffsetTargetofJson(req_json)
        qhawax_name = str(req_json['product_id']).strip()
        offsets = req_json['offsets']
        description =req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.updateOffsetsFromProductID(qhawax_name, offsets)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)    
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': ' \'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Offsets have been updated'}, 200)

@app.route('/api/save_controlled_offsets/', methods=['POST'])
def saveControlledOffsets():
    try:
        req_json = request.get_json()
        exception_helper.getControlledOffsetTargetofJson(req_json)
        qhawax_name = str(req_json['product_id']).strip()
        controlled_offsets = req_json['controlled_offsets']
        description =req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.updateControlledOffsetsFromProductID(qhawax_name, controlled_offsets)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Controlled offsets have been updated'}, 200)

@app.route('/api/save_non_controlled_offsets/', methods=['POST'])
def saveNonControlledOffsets():
    try:
        req_json = request.get_json()
        exception_helper.getNonControlledOffsetTargetofJson(req_json)
        qhawax_name = str(req_json['product_id']).strip()
        non_controlled_offsets = req_json['non_controlled_offsets']
        description =req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.updateNonControlledOffsetsFromProductID(qhawax_name, non_controlled_offsets)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Non Controlled offsets have been updated'}, 200)

