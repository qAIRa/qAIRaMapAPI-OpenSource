from flask import jsonify, make_response, request
from project.database.models import Company
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

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
        if(get_business_helper.companyNameIsNew(company_name) and get_business_helper.companyRucIsNew(ruc)):
            post_business_helper.createCompany(req_json)
            return make_response('Company has been created', 200)
        return make_response('The company name or ruc entered already exists ', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)