from flask import jsonify, make_response, request

import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import Qhawax
import project.main.business.business_helper as helper

from sqlalchemy import or_

from passlib.hash import bcrypt
from project.response_codes import RESPONSE_CODES

@app.route('/api/get_qhawax_inca/', methods=['GET'])
def getIncaQhawaxInca():
    """
    To get qHAWAX Inca Value 

    :type name: string
    :param name: qHAWAX name

    """
    try:
        name = request.args.get('name')
        inca_qhawax = helper.queryIncaQhawax(name)
        return inca_qhawax
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/get_qhawaxs_active_mode_customer/', methods=['GET'])
def getActiveQhawaxModeCustomer():
    """
    To get all active qHAWAXs that are in field in mode costumer
    
    No parameters required

    """
    qhawaxs = helper.queryQhawaxModeCustomer()
    if qhawaxs is not None:
        try:
            qhawaxs_list = [qhawax._asdict() for qhawax in qhawaxs]
            qhawaxs_list = helper.getDescriptionOfQhawaxInField(qhawaxs_list)
            return make_response(jsonify(qhawaxs_list), 200)
        except TypeError as e:
            json_message = jsonify({'error': ' \'%s\' ' % (e)})
            return make_response(json_message, 400)
    else:
        return make_response(jsonify('There are no qHAWAXs in field'), 404)


@app.route('/api/save_main_inca/', methods=['POST'])
def updateIncaData():
    """
    To save qHAWAX inca value

    Json input of following fields:

    :type name: string
    :param name: qHAWAX name

    :type value_inca: integer
    :param value_inca: qHAWAX inca value

    """
    req_json = request.get_json()
    try:
        name = str(req_json['name']).strip()
        value_inca = req_json['value_inca']
        helper.updateMainIncaInDB(value_inca, name)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format. Exception="%s"' % (e), 400)


@app.route('/api/get_time_active_qhawax/', methods=['GET'])
def getQhawaxLatestTimestamp():
    """
    To get qHAWAX Raw Measurement latest timestamp

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_name = request.args.get('qhawax_name')
    return str(helper.getQhawaxLatestTimestamp(qhawax_name))

@app.route('/api/get_time_processed_data_active_qhawax/', methods=['GET'])
def getQhawaxProcessedLatestTimestamp():
    """
    To get qHAWAX Processed Measurement latest timestamp

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_name = request.args.get('qhawax_name')
    return str(helper.getQhawaxLatestTimestampProcessedMeasurement(qhawax_name))

@app.route('/api/qhawax_status/', methods=['GET'])
def getQhawaxStatus():
    """
    Get qHAWAX Status   

    :type name: string
    :param name: qHAWAX name

    """
    try:
        name = request.args.get('name')
        qhawax_status = helper.getQhawaxStatus(name)
        return qhawax_status
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/qhawax_change_status_off/', methods=['POST'])
def sendQhawaxStatusOff():
    """
    Set qHAWAX OFF  

    Json input of following fields:

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_lost_timestamp: string
    :param qhawax_lost_timestamp: the last time qHAWAX send measurement with timezone

    """
    req_json = request.get_json()   
    helper.saveStatusOff(req_json)
    qhawax_name = str(req_json['qhawax_name']).strip()
    observation_type="Interna"
    description="Se apagó el qHAWAX"
    solution = None
    person_in_charge = None
    start_date = None
    end_date = None
    helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,start_date,end_date)
    return make_response('Success', 200)


@app.route('/api/qhawax_change_status_on/', methods=['POST'])
def sendQhawaxStatusOn():
    """
    Set qHAWAX ON   

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    req_json = request.get_json()
    qhawax_name = str(req_json['qhawax_name']).strip()
    helper.saveStatusOn(qhawax_name) 
    helper.saveTurnOnLastTime(qhawax_name)
    helper.updateMainIncaInDB(0,qhawax_name)
    observation_type="Interna"
    description="Se prendió el qHAWAX"
    solution = None
    person_in_charge = None
    start_date = None
    end_date = None
    helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,start_date,end_date)
    return make_response('Success', 200)


@app.route('/api/get_time_all_active_qhawax/', methods=['GET'])
def getTimeAllActiveQhawax():
    """
    Get Time   

    :type name: string
    :param name: qHAWAX name

    """
    name = request.args.get('name')
    installation_id = helper.getInstallationIdBaseName(name)
    values = helper.getTimeQhawaxHistory(installation_id)
    values_list = {'last_time_on': values[0], 'last_time_registration': values[1]} 
    return make_response(jsonify(values_list), 200)

@app.route('/api/create_qhawax/', methods=['POST'])
def createQhawax():
    """
    To create a qHAWAX 
    
    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_type: string
    :param qhawax_type: qHAWAX type (it could be STATIC or AEREO)

    """
    try:
        req_json = request.get_json()
        qhawax_name=str(req_json['qhawax_name']).strip() 
        qhawax_type=str(req_json['qhawax_type']).strip()
        if(helper.qhawaxNameIsNew(qhawax_name)):
            last_qhawax_id = helper.queryGetLastQhawax()
            if(last_qhawax_id==None):
                helper.createQhawax(1, qhawax_name,qhawax_type)
            else:
                helper.createQhawax(last_qhawax_id[0]+1, qhawax_name,qhawax_type)
            description="Se registró qHAWAX"
            observation_type="Interna"
            solution = None
            person_in_charge = req_json['person_in_charge']
            end_date = None
            start_date = None
            helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,start_date,end_date)
            last_gas_sensor_id = helper.queryGetLastGasSensor()
            if(last_gas_sensor_id ==None):
                helper.insertDefaultOffsets(0,qhawax_name)
            else:
                helper.insertDefaultOffsets(last_gas_sensor_id[0],qhawax_name)
            return make_response('qHAWAX & Sensors have been created', 200)
        return make_response('The qHAWAX name entered already exists ', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/get_qhawaxs/', methods=['GET'])
def getAllQhawax():
    """
    Get All qHAWAXs   

    No parameters required

    """
    qhawaxs = helper.queryAllQhawax()
    if qhawaxs is not None:
        qhawax_list = [qhawax._asdict() for qhawax in qhawaxs]
        return make_response(jsonify(qhawax_list), 200)
    else:
        return make_response(jsonify('qHAWAXs not found'), 404)

@app.route('/api/get_qhawaxs_by_mode/', methods=['GET'])
def getAllQhawaxByMode():
    """
    Get All qHAWAXs Filter by mode  

    No parameters required

    """
    mode = request.args.get('mode')
    qhawaxs_by_mode = helper.queryAllQhawaxByMode(mode)
    if qhawaxs_by_mode is not None:
        qhawax_list = [qhawax._asdict() for qhawax in qhawaxs_by_mode]
        return make_response(jsonify(qhawax_list), 200)
    else:
        return make_response(jsonify('qHAWAXs in this mode not found'), 404)


@app.route('/api/change_to_calibration/', methods=['POST'])
def qhawaxChangeToCalibration():
    """
    qHAWAX update to Calibration mode, set main inca -2 value

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        req_json = request.get_json()
        qhawax_name = str(req_json['qhawax_name']).strip()

        flag_costumer = helper.isItFieldQhawax(qhawax_name)
        if(flag_costumer == True):
            helper.saveTimeQhawaxOff(qhawax_name)
        helper.updateMainIncaInDB(-2,qhawax_name)
        helper.changeMode(qhawax_name,"Calibracion")
        observation_type="Interna"
        description="Se cambió a modo calibracion"
        solution = None
        person_in_charge = req_json['person_in_charge']
        end_date = None
        start_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,start_date,end_date)
        return make_response('Success', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/end_calibration/', methods=['POST'])
def qhawaxEndCalibration():
    """
    qHAWAX update end calibration mode, set main inca original, depends of mode (customer or stand by)

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        req_json = request.get_json()
        qhawax_name = str(req_json['qhawax_name']).strip()
        flag_costumer = helper.isItFieldQhawax(qhawax_name)
        if(flag_costumer == True):
            helper.saveTimeQhawaxOn(qhawax_name)
            helper.changeMode(qhawax_name,"Cliente")
            description="Se cambió a modo cliente"
            helper.updateMainIncaInDB(0,qhawax_name)
        else:
            helper.changeMode(qhawax_name,"Stand By")
            description="Se cambió a modo stand by"
            helper.updateMainIncaInDB(-1,qhawax_name)
        observation_type="Interna"
        solution = None
        person_in_charge = req_json['person_in_charge']
        end_date = None
        start_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,start_date,end_date)
        return make_response('Success', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)


@app.route('/api/get_time_valid_processed_data_active_qhawax/', methods=['GET'])
def getQhawaxValidProcessedLatestTimestamp():
    """
    To get qHAWAX Valid Processed Measurement latest timestamp

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    qhawax_name = request.args.get('qhawax_name')
    return str(helper.getQhawaxLatestTimestampValidProcessedMeasurement(qhawax_name))


