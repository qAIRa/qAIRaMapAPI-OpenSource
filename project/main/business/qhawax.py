from flask import jsonify, make_response, request
import project.main.same_function_helper as same_helper
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.set_up_email as set_up
from project import app, socketio
from datetime import timedelta
import dateutil.parser
import dateutil.tz
import datetime
import dateutil

@app.route('/api/get_qhawaxs/', methods=['GET'])
def getAllQhawax():
    """ Get All qHAWAXs without condition """
    try:
        qhawaxs = get_business_helper.queryAllQhawax()
        if qhawaxs is not None:
            qhawax_list = [qhawax._asdict() for qhawax in qhawaxs]
            return make_response(jsonify(qhawax_list), 200)
        return make_response(jsonify('qHAWAXs not found'), 400)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

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
        if(installation_id!=None):
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
            post_business_helper.updateMainIncaQhawaxInstallationTable(value_inca, name)
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
    jsonsend = {}
    req_json = request.get_json()
    try:
        qH_name, qH_time_off = exception_helper.getStatusOffTargetofJson(req_json)
        description = "qHAWAX off"
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
        qH_name, qH_type, in_charge, description = exception_helper.getQhawaxTargetofJson(req_json)
        post_business_helper.createQhawax(qH_name,qH_type)
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
    qhawax_time_off = datetime.datetime.now(dateutil.tz.tzutc())
    try:
        qH_name, in_charge, description = exception_helper.getChangeCalibrationFields(req_json)
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
        mode, description, main_inca = get_business_helper.getLastValuesOfQhawax(qH_name)
        if(mode == 'Cliente'): 
            post_business_helper.turnOnAfterCalibration(qH_name)
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

@app.route('/api/turn_on_based_on_loss_signal/', methods=['POST'])
def sendQhawaxStatusOnBaseOnLossSignal():
    """ Set qHAWAX ON Base On Loss Signal  - It should set last main inca value, set last last_time_off record and last last_time_on """
    req_json = request.get_json()
    try:
        qH_name, timestamp = exception_helper.getQhawaxSignalJson(req_json)
        if(same_helper.qhawaxExistBasedOnName(qH_name)):
            qhawax_state = same_helper.getQhawaxStatus(qH_name)
            mode = same_helper.getQhawaxMode(qH_name)
            comercial_name = same_helper.getComercialName(qH_name)
            if(qhawax_state=='OFF'):
                post_business_helper.saveStatusQhawaxTable(qH_name, "ON",0)
                json_email = set_up.set_email_text("qHAWAX signal", comercial_name, qH_name, mode,timestamp)
                if(mode =='Cliente'):
                    last_main_inca_value = get_data_helper.queryLastMainInca(qH_name)
                    if(last_main_inca_value!=None):
                        post_business_helper.updateMainIncaQhawaxInstallationTable(int(last_main_inca_value),qH_name)
                        post_business_helper.updateMainIncaQhawaxTable(int(last_main_inca_value),qH_name)
                    last_time_of_turn_off_binnacle = get_business_helper.queryLastTimeOffDueLackEnergy(qH_name)
                    if(last_time_of_turn_off_binnacle!=None):
                        post_business_helper.updateTimeOffWithLastTurnOff(last_time_of_turn_off_binnacle,qH_name)
                post_business_helper.writeBinnacle(qH_name,json_email['description'],json_email['person_in_charge'])
                post_business_helper.reset_on_loop(qH_name,0)
                return make_response('qHAWAX ON based on loss signal', 200)
            else:
                on_loop = int(same_helper.getQhawaxOnLoop(qH_name)) +1
                if(on_loop==20):
                    first_time = str(get_business_helper.getFirstTimeLoop(qH_name) - datetime.timedelta(hours=5))
                    json_email = set_up.set_email_text("qHAWAX loop", comercial_name, qH_name, mode,first_time)
                    post_business_helper.reset_on_loop(qH_name,0)
                else:
                    post_business_helper.reset_on_loop(qH_name,on_loop)
                    if(on_loop==1):
                        post_business_helper.record_first_time_loop(qH_name,timestamp)
            return make_response('qHAWAX is already ON ', 200)
        return make_response('qHAWAX name has not been found', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_exist/', methods=['GET'])
def verifyIfQhawaxExist():
    """ Get All qHAWAXs without condition """
    name = request.args.get('name')
    try:
        qhawax_check = same_helper.qhawaxExistBasedOnName(name)
        return str(qhawax_check)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)
