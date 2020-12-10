from flask import jsonify, make_response, request
import project.main.same_function_helper as same_helper
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app, socketio

@app.route('/api/get_qhawaxs_active_mode_customer/', methods=['GET'])
def getActiveQhawaxModeCustomer():
    """ To get all active qHAWAXs that are in field in mode costumer - No parameters required """
    try:
        qhawaxs = get_business_helper.queryQhawaxModeCustomer()
        qhawaxs_list = [qhawax._asdict() for qhawax in qhawaxs]
        return make_response(jsonify(qhawaxs_list), 200)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_time_all_active_qhawax/', methods=['GET'])
def getTimeAllActiveQhawax():
    """ Get Time All Active qHAWAX - Script """
    name = request.args.get('name')
    try:
        installation_id = same_helper.getInstallationIdBaseName(name)
        values = same_helper.getTimeQhawaxHistory(installation_id)
        if(values is not None):
            return make_response(jsonify(values), 200)
        return make_response(jsonify({'Warning':'qHAWAX name is not in field'}), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/save_main_inca/', methods=['POST'])
def updateIncaData():
    """ Server Open Source / Server Comercial - To save qHAWAX inca value """
    jsonsend = {}
    req_json = request.get_json()
    try:
        name, value_inca = exception_helper.getIncaTargetofJson(req_json)
        post_business_helper.updateMainIncaQhawaxTable(value_inca,name)
        if(same_helper.getQhawaxMode(name)=='Cliente'):
            post_business_helper.updateMainIncaInDB(value_inca, name)
        jsonsend['main_inca'] = value_inca
        jsonsend['name'] = name 
        socketio.emit('update_inca', jsonsend)
        return make_response({'Success':' save inca value'}, 200)
    except (ValueError, TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_change_status_off/', methods=['POST'])
def sendQhawaxStatusOff():
    """ Server Open Source lo apagara / Web Comercial lo pagara y enviara correo- Endpoint to set qHAWAX OFF because script detect no new data within five minutes  """
    """ Server Comercial lo apagara y enviara correo """
    jsonsend = {}
    req_json = request.get_json()
    try:
        qH_name, qH_time_off, description = exception_helper.getStatusOffTargetofJson(req_json)
        post_business_helper.saveStatusQhawaxTable(qH_name,'OFF',-1)
        if(same_helper.getQhawaxMode(qH_name)=='Cliente'):
            post_business_helper.saveStatusOffQhawaxInstallationTable(qH_name,qH_time_off)
        post_business_helper.writeBinnacle(qH_name,description,None)
        jsonsend['main_inca'] = -1
        jsonsend['name'] = qH_name 
        socketio.emit('update_inca', jsonsend)
        return make_response({'Success': 'qHAWAX off'}, 200)
    except (ValueError, TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_change_status_on/', methods=['POST'])
def sendQhawaxStatusOn():
    """ qHAWAX / Web Comercial - Set qHAWAX ON due to module reset (sensors reset) """
    jsonsend = {}
    req_json = request.get_json()
    try:
        qhawax_name = str(req_json['qhawax_name']).strip()
        description="qHAWAX turned on after a general reset"
        post_business_helper.saveStatusQhawaxTable(qhawax_name,'ON',0)
        if(same_helper.getQhawaxMode(qhawax_name)=='Cliente'):
            post_business_helper.saveTurnOnLastTime(qhawax_name)
        post_business_helper.writeBinnacle(qhawax_name,description,None)
        jsonsend['main_inca'] = 0
        jsonsend['name'] = qhawax_name 
        return make_response({'Success': 'qHAWAX ON physically'}, 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/create_qhawax/', methods=['POST'])
def createQhawax():
    """ Endpoint to create a qHAWAX """
    req_json = request.get_json()
    try:
        qH_name, qH_type, firmware_version_id, in_charge, description = exception_helper.getQhawaxTargetofJson(req_json)
        post_business_helper.createQhawax(qH_name,qH_type,firmware_version_id)
        post_business_helper.insertDefaultOffsets(qH_name)
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
        return make_response({'Success': 'qHAWAX & Sensors have been created'}, 200)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/change_to_calibration/', methods=['POST'])
def qhawaxChangeToCalibration():
    """ qHAWAX update to Calibration mode, set main inca -2 value """
    req_json = request.get_json()
    qhawax_time_off = now.replace(tzinfo=None)
    try:
        qH_name, in_charge, description = exception_helper.getChangeCalibrationFields(req_json)
        post_business_helper.saveStatusOffQhawaxTable(qH_name)
        post_business_helper.updateMainIncaQhawaxTable(-2,qH_name)
        if(same_helper.getQhawaxMode(qH_name)=='Cliente'):
            post_business_helper.saveStatusOffQhawaxInstallationTable(qH_name,qhawax_time_off)
            post_business_helper.updateMainIncaQhawaxInstallationTable(-2,qH_name)
        post_business_helper.changeMode(qH_name,"Calibracion")
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
        return make_response({'Success': 'qHAWAX have changed to calibration mode'}, 200)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/end_calibration/', methods=['POST'])
def qhawaxEndCalibration():
    """ qHAWAX update end calibration mode, set main inca original, depends of mode (customer or stand by)"""
    req_json = request.get_json()
    try:
        qH_name, in_charge = exception_helper.getEndCalibrationFields(req_json)
        mode, description, main_inca = get_business_helper.setLastValuesOfQhawax(qH_name)
        post_business_helper.changeMode(qH_name,mode)
        post_business_helper.updateMainIncaQhawaxTable(main_inca, qH_name)
        post_business_helper.updateMainIncaQhawaxInstallationTable(main_inca, qH_name)
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
        return make_response({'Success': 'qHAWAX have changed to original mode'}, 200)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
