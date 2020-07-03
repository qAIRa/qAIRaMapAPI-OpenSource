from flask_login import current_user, login_required, login_user, logout_user
from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db
from project.database.models import User, Company
import project.main.business.business_helper as helper
from sqlalchemy import or_

from project.response_codes import RESPONSE_CODES

import base64

@app.route('/api/login/', methods=['GET'])
def login():
    """
    User can login in qairamap

    :type  email: string
    :param email: user email

    :type  password: string
    :param password: user password

    """
    email_encripted = request.args.get('email')
    email_decoded = base64.b64decode(email_encripted).decode("utf-8")
    password_encripted = request.args.get('password')
    pass_decoded = base64.b64decode(password_encripted).decode("utf-8")
    user = db.session.query(User).filter_by(email=email_decoded).first()
    if user and user.validatePassword(pass_decoded):
        #Dame el nombre y id del usuario
        username = email_decoded[:email_decoded.find('@')]
        user_id = user.id
        company_id = user.company_id
        #Dame el nombre y id de la compania del usuario
        company_name= db.session.query(Company.name).filter_by(id=company_id).first()
        user_data={}
        user_data['username']=username
        user_data['user_id']=user_id
        user_data['company_name']=company_name[0]
        user_data['company_id']=company_id
        return make_response(jsonify(user_data), 200)
    else:
        return make_response(jsonify('User and password not valid'), 404)

@app.route('/api/changeCompany/', methods=['POST'])
def changeCompany():
    """
    Users can change to other company 

    Json input of following fields:

    :type  company_id: integer
    :param company_id: user company ID 

    :type  email: string
    :param email: user email

    """
    req_json = request.get_json()
    try:
        company_id = int(req_json['company_id'])
        email = str(req_json['email'])
        helper.updateCompany(company_id, email)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format. Exception="%s"' % (e), 400)

@app.route('/api/getUserCompany/', methods=['GET'])
def getUsersCompany():
    """
    List All Users with their companies

    No parameters required

    """
    users = helper.queryUsersCompany()

    if users is not None:
        user_list = [user._asdict() for user in users]
        return make_response(jsonify(user_list), 200)
    else:
        return make_response(jsonify('Users not found'), 404)

@app.route('/api/changePassword/', methods=['POST'])
def changePassword():
    """
    Users can change her/his password

    Json input of following fields:
    
    :type  email: string
    :param email: user email

    :type  old_password: string
    :param old_password: user old password

    :type  new_password: string
    :param new_password: user new password

    """
    req_json = request.get_json()
    email_encripted=str(req_json['email']).strip()
    old_password_encripted=str(req_json['old_password']).strip()
    new_password_encripted=str(req_json['new_password']).strip()

    if any(['@' in email_encripted]):
        json_message = jsonify({'error': 'You must encript email'})
        return make_response(json_message, RESPONSE_CODES['NOT_FOUND'])
    else:
        if(email_encripted!=None and old_password_encripted!=None and new_password_encripted!=None):
            email_decoded = base64.b64decode(email_encripted).decode("utf-8")
            old_pass_decoded = base64.b64decode(old_password_encripted).decode("utf-8")
            new_pass_decoded = base64.b64decode(new_password_encripted).decode("utf-8")
            user = db.session.query(User).filter_by(email=email_decoded).first()
            try:
                if user and user.validatePassword(old_pass_decoded):
                    helper.changePassword(user,new_pass_decoded)
                    json_message = jsonify({'OK': 'Password have been changed'})
                    return make_response(json_message, RESPONSE_CODES['OK'])
                else:
                    json_message = jsonify({'error': 'Incorrect Password'})
                    return make_response(json_message, RESPONSE_CODES['NOT_FOUND'])
            except Exception as e:
                json_message = jsonify({'error': 'You have entered an invalid email'})
                return make_response(json_message, RESPONSE_CODES['NOT_FOUND'])	
        else:
            json_message = jsonify({'error': 'Characters not valid'})
            return make_response(json_message, RESPONSE_CODES['NOT_FOUND'])


@app.route('/api/createUser/', methods=['POST'])
def createUser():
    """
    qAIRA administrator can create new users

    Json input of following fields:

    :type  email: string
    :param email: user email

    :type  company_id: string
    :param company_id: user company ID

    :type  encripted_pasword: string
    :param encripted_pasword: user password

    """
    try:
        req_json = request.get_json()
        user_email=str(req_json['email']).strip()  
        company_id=int(req_json['company_id'])
        encripted_password=str(req_json['encripted_pasword']).strip()
        password = base64.b64decode(encripted_password).decode("utf-8")
        var_company = helper.getCompany(company_id)
        helper.createUser(user_email,company_id,var_company.name,var_company.email_group, password)
        return make_response('User has been created', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

	
	



