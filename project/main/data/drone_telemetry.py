import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
from flask import jsonify, make_response, request
from project import app, socketio

@app.route('/api/send_telemetry_andean_drone/', methods=['POST'])
def handleTelemetry():
    global drone_telemetry
    try:
        data_json = request.get_json()
        token = data_json['token'] if (data_json['token']=='droneandino123') else None
        room = data_json['room'] #El room es el qhawax ID
        telemetry = data_json['telemetry']
    except KeyError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    telemetry['ID'] = room
    socketio.emit(telemetry['ID'] + '_telemetry', data_json)
    drone_telemetry = telemetry
    post_data_helper.storeLogs(telemetry, room)
    return {'success': 'Telemetry sent from drone: "%s"' % (telemetry)}

