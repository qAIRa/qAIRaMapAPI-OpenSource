from flask import jsonify, make_response, request
import project.main.same_function_helper as same_helper
import project.main.exceptions as exception_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
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
        all_qhawaxs = get_business_helper.queryAllQhawax()
        if (all_qhawaxs!=[]):
            return make_response(jsonify(all_qhawaxs), 200)
        return make_response(jsonify({'Warning':'qHAWAXs not found'}), 400)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_qhawaxs_active_mode_customer/', methods=['GET'])
def getActiveQhawaxModeCustomer():
    """ To get all active qHAWAXs that are in field in mode costumer - No parameters required """
    try:
        customer_qhawaxs = get_business_helper.queryQhawaxModeCustomer()
        if(customer_qhawaxs!=[]):
            return make_response(jsonify(customer_qhawaxs), 200)
        return make_response(jsonify({'Warning':'qHAWAXs not found'}), 400)
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_time_all_active_qhawax/', methods=['GET'])
def getTimeAllActiveQhawax():
    """ Get Time All Active qHAWAX - Script """
    name = request.args.get('name')
    try:
        values = same_helper.getTimeQhawaxHistory(name)
        if(values is not None):
            return make_response(jsonify(values), 200)
        return make_response(jsonify({'Warning':'qHAWAX name is not in field'}), 400)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_exist/', methods=['GET'])
def verifyIfQhawaxExist():
    """ Verify if qHAWAX exist """
    name = request.args.get('name')
    try:
        return str(same_helper.qhawaxExistBasedOnName(name))
    except TypeError as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_status/', methods=['GET'])
def getQhawaxStatus():
    """ Get qHAWAX Status """
    name = request.args.get('name')
    try:
        return str(same_helper.getQhawaxStatus(name)) if (same_helper.getQhawaxStatus(name)!=None) else make_response({'Warning': 'qHAWAX name has not been found'}, 400)
    except Exception as e:
        json_message = jsonify({'error': ' \'%s\' ' % (e)})
        return make_response(json_message, 400)

@app.route('/api/save_main_inca/', methods=['POST'])
def updateIncaData():
    """ Server Open Source / Server Comercial - To save qHAWAX inca value """
    jsonsend = {}
    req_json = request.get_json()
    try:
        name, value_inca = exception_helper.getIncaTargetofJson(req_json)
        post_business_helper.updateMainIncaQhawaxTable(value_inca,name)
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
    description = "qHAWAX off"
    try:
        qH_name = exception_helper.getStatusOffTargetofJson(req_json)
        post_business_helper.saveStatusQhawaxTable(qH_name,'OFF',-1)
        lessfive = get_data_helper.getQhawaxLatestTimestampProcessedMeasurement(qH_name)
        post_business_helper.saveStatusOffQhawaxInstallationTable(qH_name,lessfive)
        post_business_helper.writeBinnacle(qH_name,description,'API')
        jsonsend['main_inca'] = -1
        jsonsend['name'] = qH_name
        socketio.emit('update_inca', jsonsend)
        type = same_helper.queryQhawaxType(qH_name)
        if (type == 'MOBILE_EXT'):
            #print("I am a Mobile qHAWAX!")
            finish_trip = datetime.datetime.now(dateutil.tz.tzutc())
            # record end trip
            post_data_helper.recordEndTrip(qH_name, "Turned off by API")
            socketio.emit(qH_name + '_finishTrip', str(finish_trip))

        return make_response({'Success': 'qHAWAX OFF'}, 200)
    except (ValueError, TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/qhawax_change_status_on/', methods=['POST'])
def sendQhawaxStatusOn():
    """ qHAWAX / Web Comercial - Set qHAWAX ON due to module reset (sensors reset) """
    jsonsend = {}
    req_json = request.get_json()
    description="qHAWAX turned on after a general reset"
    try:
        qhawax_name = str(req_json['qhawax_name']).strip()
        post_business_helper.saveStatusQhawaxTable(qhawax_name,'ON',0)
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
    description = "qHAWAX has been changed to calibration mode"
    try:
        qH_name, in_charge = exception_helper.getChangeCalibrationFields(req_json)
        post_business_helper.updateMainIncaQhawaxTable(-2,qH_name)
        post_business_helper.saveStatusOffQhawaxInstallationTable(qH_name,qhawax_time_off)
        post_business_helper.updateMainIncaQhawaxInstallationTable(-2,qH_name)
        post_business_helper.changeMode(qH_name,"Calibration")
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
        return make_response({'Success': 'qHAWAX has been changed to calibration mode - open'}, 200)
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
        post_business_helper.updateMainIncaQhawaxTable(main_inca, qH_name)
        post_business_helper.updateMainIncaQhawaxInstallationTable(main_inca, qH_name)
        post_business_helper.changeMode(qH_name,mode)
        post_business_helper.writeBinnacle(qH_name,description,in_charge)
        return make_response({'Success': 'qHAWAX has been changed to original mode - open'}, 200)
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
        qhawax_state = same_helper.getQhawaxStatus(qH_name)
        description='qHAWAX turned on after a loss of signal'
        json_email = {'description':description,'person_in_charge':'Firmware'}
        if(qhawax_state is not None):
            mode = same_helper.getQhawaxMode(qH_name)
            on_loop = int(same_helper.getQhawaxOnLoop(qH_name)) +1
            if(qhawax_state=='OFF'):
                post_business_helper.saveStatusQhawaxTable(qH_name, "ON",0)
                post_business_helper.setLastMeasurementOfQhawax(qH_name)
                post_business_helper.writeBinnacle(qH_name,json_email['description'],json_email['person_in_charge'])
                post_business_helper.resetOnLoop(qH_name,0)
                return make_response({'Success': description}, 200)
            else:
                post_business_helper.resetOnLoop(qH_name,0) if(on_loop==20) else post_business_helper.resetOnLoop(qH_name,on_loop)
                if(on_loop==1):
                    post_business_helper.recordFirstTimeLoop(qH_name,timestamp)
                return make_response({'Success': 'qHAWAX is already ON'}, 200)
        return make_response({'Warning': 'qHAWAX name has not been found'}, 400)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
