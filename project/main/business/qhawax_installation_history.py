from flask import jsonify, make_response, request

import datetime
import dateutil.parser
import dateutil.tz

from project import app, db, socketio
from project.database.models import Qhawax
import project.main.business.business_helper as helper

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
    try:
        data_json = request.get_json()
        qhawax_id = data_json['qhawax_id']
        helper.storeNewQhawaxInstallation(data_json)
        helper.setOccupiedQhawax(qhawax_id)
        helper.setModeCustomer(qhawax_id)
        qhawax_name = helper.getQhawaxName(qhawax_id)
        description="Se registró qHAWAX en campo"
        observation_type="Interna"
        solution = None
        person_in_charge = data_json['person_in_charge']
        end_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

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
    try:
        data_json = request.get_json()
        qhawax_id = data_json['qhawax_id']
        installation_id = helper.getInstallationId(qhawax_id)
        helper.saveEndWorkFieldDate(installation_id, data_json['end_date'])
        helper.setAvailableQhawax(qhawax_id)
        qhawax_name = helper.getQhawaxName(qhawax_id)
        helper.changeMode(qhawax_name, "Stand By")
        description="Se registró fin de trabajo en campo"
        observation_type="Interna"
        solution = None
        person_in_charge = data_json['person_in_charge']
        end_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/AllQhawaxByCompany/', methods=['GET'])
def getQhawaxByCompany():
    """
    Get list of qHAWAXs filter by company ID

    The response will refer to the modules of that company

    :type  company_id: integer
    :param company_id: company ID

    """
    company_id = request.args.get('company_id')
    
    qhawax_in_field_by_company = helper.queryQhawaxInFieldByCompany(company_id)
    if qhawax_in_field_by_company is not None:
        qhawax_in_field_by_company_list = [installation._asdict() for installation in qhawax_in_field_by_company]
        return make_response(jsonify(qhawax_in_field_by_company_list), 200)
    else:
        return make_response(jsonify('qHAWAXs not found'), 404)


@app.route('/api/GetInstallationDate/', methods=['GET'])
def getInstallationDate():
    """
    Get installation Data of qHAWAX in field

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID
    
    """
    try:
        qhawax_id = request.args.get('qhawax_id')
        if(int(qhawax_id)!=7 and int(qhawax_id)!=8 and int(qhawax_id)!=10 and int(qhawax_id)!=11 and int(qhawax_id)!=12 and int(qhawax_id)!=13 and int(qhawax_id)!=14):
            installation_date = helper.getInstallationDateByQhawaxID(qhawax_id)
            installation_id = helper.getInstallationId(qhawax_id)
            first_timestamp = helper.getFirstTimestampValidProcessed(installation_id)
            if(first_timestamp!=None):
                if(first_timestamp>installation_date):
                    return str(first_timestamp)
                else:
                    return str(installation_date)
            else:
                return str(installation_date)
        else:
            return '2020-03-19 12:00:00.255258'
    except Exception as e:
        print(e)
        return make_response('No Installation Date', 400)

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
        qhawax_id = data_json['qhawax_id']
        helper.updateQhawaxInstallation(data_json)
        qhawax_name = helper.getQhawaxName(qhawax_id)
        description="Se modificaron algunos campos de la instalación del qHAWAX"
        observation_type="Interna"
        solution = None
        person_in_charge = data_json['person_in_charge']
        end_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

