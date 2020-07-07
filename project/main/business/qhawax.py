from flask import jsonify, make_response, request

import datetime
import dateutil.parser
import dateutil.tz

from project import app, db, socketio
from project.database.models import Qhawax
import project.main.business.business_helper as helper

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

@app.route('/api/qhawax_change_status_off/', methods=['POST'])
def sendQhawaxStatusOff():
    """
    Set qHAWAX OFF  

    Json input of following fields:

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_lost_timestamp: string
    :param qhawax_lost_timestamp: the last time qHAWAX send measurement

    """
    req_json = request.get_json()   
    helper.saveStatusOff(req_json)
    qhawax_name = str(req_json['qhawax_name']).strip()
    observation_type="Interna"
    description="Se apagó el qHAWAX"
    solution = None
    person_in_charge = None
    end_date = None
    helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
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
    end_date = None
    helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
    return make_response('Success', 200)

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
            helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
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


@app.route('/api/change_to_calibration/', methods=['POST'])
def qhawaxChangeToCalibration():
    """
    qHAWAX update to Calibration mode

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        req_json = request.get_json()
        qhawax_name = str(req_json['qhawax_name']).strip()
        #actualizar los incas en qhawax y qhawax installation
        helper.updateMainIncaInDB(-2,qhawax_name)
        helper.changeMode(qhawax_name,"Calibracion")
        observation_type="Interna"
        description="Se cambió a modo calibracion"
        solution = None
        person_in_charge = req_json['person_in_charge']
        end_date = None
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
        return make_response('Success', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/end_calibration/', methods=['POST'])
def qhawaxEndCalibration():
    """
    qHAWAX update end calibration mode

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        req_json = request.get_json()
        qhawax_name = str(req_json['qhawax_name']).strip()
        flag_costumer = helper.isItFieldQhawax(qhawax_name)
        if(flag_costumer == True):
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
        helper.writeBitacora(qhawax_name,observation_type,description,solution,person_in_charge,end_date)
        return make_response('Success', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)


