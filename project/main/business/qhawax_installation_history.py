from flask import jsonify, make_response, request
from project.database.models import Qhawax
import project.main.same_function_helper as same_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/newQhawaxInstallation/', methods=['POST'])
def newQhawaxInstallation():
    """
    To create a qHAWAX in Field 
    
    Json input of following fields:
    
    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type  lat: double
    :param lat: latitude of qHAWAX location

    :type  lon: double
    :param lon: longitude of qHAWAX location

    :type  instalation_date: timestamp
    :param instalation_date: qHAWAX Installation Date

    :type  link_report: string
    :param link_report: link of installation report

    :type  observations: string
    :param observations: installation detail

    :type  district: string
    :param district: district where qHAWAX is located

    :type  comercial_name: string
    :param comercial_name: qHAWAX comercial name

    :type  address: string
    :param address: address where qHAWAX is located

    :type  company_id: integer
    :param company_id: company ID to which qHAWAX belongs

    :type  eca_noise_id: integer
    :param eca_noise_id: ID of type of qHAWAX zone

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type  connection_type: string
    :param connection_type: Type of qHAWAX connection

    :type  index_type: string
    :param index_type: Type of qHAWAX index

    :type  measuring_height: integer
    :param measuring_height: Height of qHAWAX in field

    :type  season: string
    :param season: season of the year when the module was deployed

    """
    data_json = request.get_json()
    try:
        qhawax_id = data_json['qhawax_id']
        post_business_helper.storeNewQhawaxInstallation(data_json)
        post_business_helper.setOccupiedQhawax(qhawax_id)
        post_business_helper.setModeCustomer(qhawax_id)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        description="Se registró qHAWAX en campo"
        person_in_charge = data_json['person_in_charge']
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        return make_response('Success: Save new qHAWAX in field', 200)
    except Exception as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/saveEndWorkField/', methods=['POST'])
def saveEndWorkField():
    """
    Save last date of qHAWAX in field
    
    Json input of following fields:

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type  end_date: timestamp
    :param end_date: end date of qHAWAX installation

    """
    data_json = request.get_json()
    try:
        qhawax_id = data_json['qhawax_id']
        end_date = data_json['end_date']
        post_business_helper.saveEndWorkFieldDate(qhawax_id, end_date)
        post_business_helper.setAvailableQhawax(qhawax_id)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        post_business_helper.changeMode(qhawax_name, "Stand By")
        description="Se registró fin de trabajo en campo"
        person_in_charge = data_json['person_in_charge']
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        return make_response('Success: Save qHAWAX last day in field', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/AllQhawaxInMap/', methods=['GET'])
def getQhawaxInMap():
    """
    Get list of qHAWAXs filter by company ID

    Filter by company ID, the response will refer to the modules of that company

    :type  company_id: integer
    :param company_id: company ID

    """
    try:
        qhawax_in_field = get_business_helper.queryQhawaxInFieldInPublicMode()
        if qhawax_in_field is not None:
            qhawax_in_field_list = [installation._asdict() for installation in qhawax_in_field]
            return make_response(jsonify(qhawax_in_field_list), 200)
        else:
            return make_response(jsonify('qHAWAXs not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/GetInstallationDate/', methods=['GET'])
def getInstallationDate():
    """
    Get installation date of qHAWAX in field

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID
    
    """
    try:
        qhawax_id = int(request.args.get('qhawax_id'))
        installation_date = get_business_helper.getInstallationDate(qhawax_id)
        if (installation_date != None):
            first_timestamp = get_business_helper.getFirstTimestampValidProcessed(qhawax_id)
            if(first_timestamp!=None):
                if(first_timestamp>installation_date):
                    return str(first_timestamp)
                else:
                    return str(installation_date)
            else:
                return str(installation_date)
        else:
            return make_response(jsonify("qHAWAX ID "+str(qhawax_id)+" has not been found in field"), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/updateQhawaxInstallation/', methods=['POST'])
def updateQhawaxInstallation():
    """
    To create a qHAWAX in Field 
    
    Json input of following fields:
    
    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type  lat: double
    :param lat: latitude of qHAWAX location

    :type  lon: double
    :param lon: longitude of qHAWAX location

    :type  link_report: string
    :param link_report: link of installation report

    :type  observations: string
    :param observations: installation detail

    :type  district: string
    :param district: district where qHAWAX is located

    :type  comercial_name: string
    :param comercial_name: qHAWAX comercial name

    :type  address: string
    :param address: address where qHAWAX is located

    :type  company_id: integer
    :param company_id: company ID to which qHAWAX belongs

    :type  eca_noise_id: integer
    :param eca_noise_id: ID of type of qHAWAX zone

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type  connection_type: string
    :param connection_type: Type of qHAWAX connection

    :type  measuring_height: integer
    :param measuring_height: Height of qHAWAX in field

    :type  season: string
    :param season: season of the year when the module was deployed

    """
    try:
        data_json = request.get_json()
        qhawax_id = int(data_json['qhawax_id'])
        post_business_helper.updateQhawaxInstallation(data_json)
        qhawax_name = same_helper.getQhawaxName(qhawax_id)
        description="Se modificaron algunos campos de la instalación del qHAWAX"
        person_in_charge = data_json['person_in_charge']
        helper.writeBitacora(qhawax_name,description,person_in_charge)
        return make_response('Sucess: Update data of qHAWAX in field', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

