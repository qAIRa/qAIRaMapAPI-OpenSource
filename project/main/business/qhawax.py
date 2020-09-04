from flask import jsonify, make_response, request
import project.main.same_function_helper as same_helper
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app, socketio

#@app.route('/api/get_qhawax_inca/', methods=['GET'])
def getIncaQhawaxInca():
    """
    To get qHAWAX Inca Value 

    :type name: string
    :param name: qHAWAX name

    """
    try:
        name = request.args.get('name')
        inca_qhawax = get_business_helper.queryIncaQhawax(name)
        if(inca_qhawax is not None):
            return make_response(jsonify(inca_qhawax), 200)
        return make_response({'Warning':'qHAWAX name has not been found'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/get_qhawaxs_active_mode_customer/', methods=['GET'])
def getActiveQhawaxModeCustomer():
    """
    To get all active qHAWAXs that are in field in mode costumer
    
    No parameters required

    """
    try:
        qhawaxs = get_business_helper.queryQhawaxModeCustomer()
        if qhawaxs is not []:
            qhawaxs_list = [qhawax._asdict() for qhawax in qhawaxs]
            return make_response(jsonify(qhawaxs_list), 200)
        return make_response({'Warning':'There are no qHAWAXs in field'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/save_main_inca/', methods=['POST'])
def updateIncaData():
    """
    To save qHAWAX inca value

    Json input of following fields:

    :type name: string
    :param name: qHAWAX name

    :type value_inca: integer
    :param value_inca: qHAWAX inca value

    """
    jsonsend = {}
    try:
        req_json = request.get_json()
        exception_helper.getIncaTargetofJson(req_json)
        name = str(req_json['name']).strip()
        value_inca = req_json['value_inca']
        post_business_helper.updateMainIncaQhawaxTable(value_inca,name)
        if(get_business_helper.getQhawaxMode(name)=='Cliente'):
            post_business_helper.updateMainIncaInDB(value_inca, name)
        jsonsend['main_inca'] = value_inca
        jsonsend['name'] = name 
        socketio.emit('update_inca', jsonsend)
        return make_response({'Success':' save inca value'}, 200)
    except (ValueError, TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/qhawax_change_status_off/', methods=['POST'])
def sendQhawaxStatusOff():
    """
    Endpoint to set qHAWAX OFF because script detect no new data within five minutes

    Json input of following fields:

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_lost_timestamp: string
    :param qhawax_lost_timestamp: the last time qHAWAX send measurement with timezone

    :type description: string
    :param description: qHAWAX description

    :type person_in_charge: string
    :param person_in_charge: person who did this action

    """
    
    jsonsend = {}
    try:
        req_json = request.get_json()
        exception_helper.getStatusOffTargetofJson(req_json)
        name = str(req_json['qhawax_name']).strip()
        qhawax_time_off = req_json['qhawax_lost_timestamp']
        description = req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.saveStatusOffQhawaxTable(name)
        if(get_business_helper.getQhawaxMode(name)=='Cliente'):
            post_business_helper.saveStatusOffQhawaxInstallationTable(name,qhawax_time_off)
        post_business_helper.writeBinnacle(name,description,person_in_charge)
        jsonsend['main_inca'] = -1
        jsonsend['name'] = name 
        socketio.emit('update_inca', jsonsend)
        return make_response({'Success': 'qHAWAX off'}, 200)
    except (ValueError, TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/qhawax_change_status_on/', methods=['POST'])
def sendQhawaxStatusOn():
    """
    Set qHAWAX ON due to module reset (sensors reset) 

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type description: string
    :param description: qHAWAX description

    :type person_in_charge: string
    :param person_in_charge: person who did this action

    """
    
    jsonsend = {}
    try:
        req_json = request.get_json()
        exception_helper.getStatusOnTargetofJson(req_json)
        qhawax_name = str(req_json['qhawax_name']).strip()
        description = req_json['description']
        person_in_charge = req_json['person_in_charge']
        post_business_helper.saveStatusOnTable(qhawax_name)
        if(get_business_helper.getQhawaxMode(qhawax_name)=='Cliente'):
            post_business_helper.saveTurnOnLastTime(qhawax_name)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        jsonsend['main_inca'] = 0
        jsonsend['name'] = qhawax_name 
        return make_response({'Success': 'qHAWAX ON physically'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/get_time_all_active_qhawax/', methods=['GET'])
def getTimeAllActiveQhawax():
    """
    Get Time All Active qHAWAX - Script   

    :type name: string
    :param name: qHAWAX name

    """
    try:
        name = request.args.get('name')
        values = get_business_helper.getTimeQhawaxHistory(name)
        if(values is not None):
            values_list = {'last_time_on': values[0], 'last_time_registration': values[1]} 
            return make_response(jsonify(values_list), 200)
        return make_response(jsonify({'Warning':'qHAWAX name is not in field'}), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/create_qhawax/', methods=['POST'])
def createQhawax():
    """
    To create a qHAWAX 
    
    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type qhawax_type: string
    :param qhawax_type: qHAWAX type (it could be STATIC or AEREO)
    
    :type description: string
    :param description: qHAWAX description

    :type person_in_charge: string
    :param person_in_charge: person who did this action

    """
    try:
        req_json = request.get_json()
        exception_helper.getQhawaxTargetofJson(req_json)
        qhawax_name=str(req_json['qhawax_name']).strip() 
        qhawax_type=str(req_json['qhawax_type']).strip()
        person_in_charge = req_json['person_in_charge']
        description = req_json['description']
        last_qhawax_id = get_business_helper.queryGetLastQhawax()
        if(last_qhawax_id==None):
            post_business_helper.createQhawax(1, qhawax_name,qhawax_type)
        else:
            post_business_helper.createQhawax(last_qhawax_id[0]+1, qhawax_name,qhawax_type)
        last_gas_sensor_id = get_business_helper.queryGetLastGasSensor()
        if(last_gas_sensor_id ==None):
            post_business_helper.insertDefaultOffsets(0,qhawax_name)
        else:
            post_business_helper.insertDefaultOffsets(last_gas_sensor_id[0],qhawax_name)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        return make_response({'Success': 'qHAWAX & Sensors have been created'}, 200)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/change_to_calibration/', methods=['POST'])
def qhawaxChangeToCalibration():
    """
    qHAWAX update to Calibration mode, set main inca -2 value

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type description: string
    :param description: qHAWAX description

    :type person_in_charge: string
    :param person_in_charge: username who change mode

    """
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['qhawax_name']).strip()
        person_in_charge = req_json['person_in_charge']
        description = req_json['description']
        qhawax_time_off = now.replace(tzinfo=None)
        post_business_helper.saveStatusOffQhawaxTable(qhawax_name)
        post_business_helper.updateMainIncaQhawaxTable(-2,qhawax_name)
        if(get_business_helper.getQhawaxMode(qhawax_name)=='Cliente'):
            post_business_helper.saveStatusOffQhawaxInstallationTable(name,qhawax_time_off)
            post_business_helper.updateMainIncaQhawaxInstallationTable(-2,qhawax_name)
        post_business_helper.changeMode(qhawax_name,"Calibracion")
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        return make_response({'Success': 'qHAWAX have changed to calibration mode'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/end_calibration/', methods=['POST'])
def qhawaxEndCalibration():
    """
    qHAWAX update end calibration mode, set main inca original, depends of mode (customer or stand by)

    Json input of following fields:
    
    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    :type person_in_charge: string
    :param person_in_charge: username who change mode

    """
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['qhawax_name']).strip()
        person_in_charge = str(req_json['person_in_charge'])
        flag_costumer = get_business_helper.isItFieldQhawax(qhawax_name)
        if(flag_costumer == True):
            post_business_helper.turnOnAfterCalibration(qhawax_name)
            mode = "Cliente"
            description="Se cambió a modo cliente"
            main_inca = 0
        else:
            mode = "Stand By"
            description="Se cambió a modo stand by"
            main_inca = -1
        post_business_helper.changeMode(qhawax_name,mode)
        post_business_helper.updateMainIncaQhawaxTable(main_inca, qhawax_name)
        post_business_helper.updateMainIncaQhawaxInstallationTable(main_inca, qhawax_name)
        post_business_helper.writeBinnacle(qhawax_name,description,person_in_charge)
        return make_response({'Success': 'qHAWAX have changed to original mode'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
        
#@app.route('/api/get_time_processed_data_active_qhawax/', methods=['GET'])
def getQhawaxProcessedLatestTimestamp():
    """
    To get qHAWAX Processed Measurement latest timestamp

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        qhawax_name = request.args.get('qhawax_name')
        processed_timestamp = get_business_helper.getLatestTimeInProcessedMeasurement(qhawax_name)
        if(processed_timestamp is not None):
            if(processed_timestamp is ""):
                return make_response({'Warning':' qHAWAX name has not been found in Processed Measurement'},200)
            return make_response(str(processed_timestamp),200)
        return make_response({'Warning': 'qHAWAX name has not been found qHAWAX table'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/get_time_valid_processed_data_active_qhawax/', methods=['GET'])
def getQhawaxValidProcessedLatestTimestamp():
    """
    To get qHAWAX Valid Processed Measurement latest timestamp

    :type qhawax_name: string
    :param qhawax_name: qHAWAX name

    """
    try:
        qhawax_name = request.args.get('qhawax_name')
        valid_processed_timestamp = get_business_helper.getLatestTimeInValidProcessed(qhawax_name)
        if(valid_processed_timestamp is not None):
            if(valid_processed_timestamp is ""):
                return make_response({'Warning':' qHAWAX name has not been found in Valid Processed Measurement'},200)
            return make_response(str(valid_processed_timestamp),200)
        return make_response({'Warning': 'qHAWAX name has not been found qHAWAX table'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

#@app.route('/api/qhawax_status/', methods=['GET'])
def getQhawaxStatus():
    """
    Get qHAWAX Status   

    :type name: string
    :param name: qHAWAX name

    """
    try:
        name = request.args.get('name')
        qhawax_status = get_business_helper.getQhawaxStatus(name)
        if (qhawax_status is not None):
            return qhawax_status
        return None
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
