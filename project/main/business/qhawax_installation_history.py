from flask import jsonify, make_response, request

import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import Qhawax
import project.main.business.business_helper as helper
from sqlalchemy import or_

@app.route('/api/AllQhawaxInField/', methods=['GET'])
def getAllQhawaxInField():
    """
    Get all qHAWAX in field

    No parameters required

    """
    qhawax_in_field = helper.queryQhawaxInField()
    if qhawax_in_field is not None:
        qhawax_in_field_list = [installation._asdict() for installation in qhawax_in_field]
        qhawax_in_field_list = helper.setQhawaxName(qhawax_in_field_list)
        return make_response(jsonify(qhawax_in_field_list), 200)
    else:
        return make_response(jsonify('Measurements not found'), 404)

@app.route('/api/AllQhawaxByCompany/', methods=['GET'])
def getQhawaxByCompany():
    """
    Get list of qHAWAXs filter by company ID

    Filter by company ID, the response will refer to the modules of that company

    :type  company_id: integer
    :param company_id: company ID

    """
    company_id = request.args.get('company_id')
     
    qhawax_in_field_by_company = helper.queryQhawaxInFieldByCompanyInPublicMode(company_id)
    if qhawax_in_field_by_company is not None:
        qhawax_in_field_by_company_list = [installation._asdict() for installation in qhawax_in_field_by_company]
        return make_response(jsonify(qhawax_in_field_by_company_list), 200)
    else:
        return make_response(jsonify('qHAWAXs not found'), 404)


@app.route('/api/GetInstallationDate/', methods=['GET'])
def getInstallationDate():
    """
    Get installation date of qHAWAX in field

    :type  qhawax_id: integer
    :param qhawax_id: qHAWAX ID
    
    """
    try:
        qhawax_id = request.args.get('qhawax_id')
        installation_date = helper.getInstallationDateByQhawaxID(qhawax_id)
        if installation_date != None:
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
            return make_response(jsonify("qHAWAX is not in field"), 200)

    except Exception as e:
        print(e)
        return make_response('No Installation Date', 400)


@app.route('/api/AllCustomerQhawax/', methods=['GET'])
def getAllCustomerQhawax():
    """
    Get a list of Customer qHAWAXs filter by company ID

    It does not care if it is public or private

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

