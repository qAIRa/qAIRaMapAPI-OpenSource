from flask import jsonify, make_response, request
import project.main.same_function_helper as same_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/newQhawaxInstallation/', methods=['POST'])
def newQhawaxInstallation():
    """
    To create a qHAWAX in Field 

    """
    data_json = request.get_json()
    try:
        qhawax_id = data_json['qhawax_id']
        qhawax_id = data_json['description']
        person_in_charge = data_json['person_in_charge']
        post_business_helper.storeNewQhawaxInstallation(data_json)
        post_business_helper.setOccupiedQhawax(qhawax_id)
        post_business_helper.setModeCustomer(qhawax_id)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
    except Exception as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success': 'Save new qHAWAX in field'}, 200)


@app.route('/api/saveEndWorkField/', methods=['POST'])
def saveEndWorkField():
    """
    Save last date of qHAWAX in field

    """
    data_json = request.get_json()
    try:
        qhawax_id = data_json['qhawax_id']
        end_date = data_json['end_date']
        description = data_json['description']
        person_in_charge = data_json['person_in_charge']
        post_business_helper.saveEndWorkFieldDate(qhawax_id, end_date)
        post_business_helper.setAvailableQhawax(qhawax_id)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        post_business_helper.changeMode(qhawax_name, "Stand By")
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response('Success: Save qHAWAX last day in field', 200)


@app.route('/api/AllQhawaxInMap/', methods=['GET'])
def getQhawaxInMap():
    """
    Get list of qHAWAXs filter by company ID

    """
    try:
        qhawax_in_field = get_business_helper.queryQhawaxInFieldInPublicMode()
        qhawax_in_field_list = [installation._asdict() for installation in qhawax_in_field]
        return make_response(jsonify(qhawax_in_field_list), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/GetInstallationDate/', methods=['GET'])
def getInstallationDate():
    """
    Get installation date of qHAWAX in field
    
    """
    try:
        qhawax_id = int(request.args.get('qhawax_id'))
        installation_date = get_business_helper.getInstallationDate(qhawax_id)
        first_timestamp = get_business_helper.getFirstTimestampValidProcessed(qhawax_id)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        if (installation_date != None):
            if(first_timestamp!=None):
                if(first_timestamp>installation_date):
                    return str(first_timestamp)
                return str(installation_date)
            return str(installation_date)
        return make_response({'Success ':'qHAWAX ID '+str(qhawax_id)+' has not been found in field'}, 200)

@app.route('/api/updateQhawaxInstallation/', methods=['POST'])
def updateQhawaxInstallation():
    """
    To create a qHAWAX in Field 

    """
    try:
        data_json = request.get_json()
        qhawax_id = int(data_json['qhawax_id'])
        description = int(data_json['description'])
        person_in_charge = data_json['person_in_charge']
        post_business_helper.updateQhawaxInstallation(data_json)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        helper.writeBitacora(qhawax_name,description,person_in_charge)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Sucess': 'Update data of qHAWAX in field'}, 200)

