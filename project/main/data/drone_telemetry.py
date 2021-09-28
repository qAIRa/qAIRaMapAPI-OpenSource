import datetime
from datetime import timedelta

import dateutil.parser
import dateutil.tz
from flask import jsonify, make_response, request

import project.main.business.get_business_helper as get_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
from project import app, socketio


@app.route("/api/send_telemetry_andean_drone/", methods=["POST"])
def handleTelemetry():
    global drone_telemetry
    try:
        data_json = request.get_json()
        token = (
            data_json["token"]
            if (data_json["token"] == "droneandino123")
            else None
        )
        room = data_json["room"]  # El room es el qhawax ID
        telemetry = data_json["telemetry"]
    except KeyError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
    if get_business_helper.isAerealQhawax(room) == True:
        telemetry["ID"] = room
        socketio.emit(room + "_telemetry", telemetry)
        drone_telemetry = telemetry
        post_data_helper.storeLogs(telemetry, room)
        return make_response(
            {"success": "Telemetry sent from drone: " + str(room)}, 200
        )
    return make_response(
        {"warning": "qHAWAX " + str(room) + " is not aereal "}, 400
    )


@app.route("/api/telemetry_andean_drone/", methods=["GET"])
def getTelemetryDataFromAndeanDrone():
    """Lists all measurements of processed measurement table within the initial and final date"""
    qhawax_name = request.args.get("qhawax_name")
    initial_timestamp = datetime.datetime.strptime(
        request.args.get("initial_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    final_timestamp = datetime.datetime.strptime(
        request.args.get("final_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    try:
        telemetry = get_data_helper.queryDBTelemetry(
            qhawax_name, initial_timestamp, final_timestamp
        )
        if telemetry is not None:
            return make_response(jsonify(telemetry), 200)
        return make_response(jsonify("Telemetry not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
