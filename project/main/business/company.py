from flask import jsonify, make_response, request

from project import app
from project.database.models import Company
import project.main.business.business_helper as helper


@app.route('/api/create_company/', methods=['POST'])
def createCompany():
    """
    adds a company 
    
    Json input of following fields:
    
    :type company_name: string
    :param company_name: company name to add to the database

    :type email_group: string
    :param email_group: email group to differentiate between one company and another

    """
    try:
        req_json = request.get_json()
        company_name=str(req_json['company_name']).strip()
        ruc=str(req_json['ruc']).strip()
        if(helper.companyNameIsNew(company_name) and helper.companyRucIsNew(ruc)):
            helper.createCompany(req_json)
            return make_response('Company has been created', 200)
        return make_response('The company name or ruc entered already exists ', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)