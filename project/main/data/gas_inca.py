import datetime

import dateutil.parser
import dateutil.tz
from flask import jsonify, make_response, request

import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
from project import app, socketio


@app.route("/api/saveGasInca/", methods=["POST"])
def handleGasInca():
    """POST: Records gas and dust measurement in gas inca table"""
    try:
        data_json = request.get_json()
        post_data_helper.storeGasIncaInDB(data_json)
        socketio.emit("gas_inca_summary", data_json)
        return make_response("OK", 200)
    except Exception as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/last_gas_inca_data/", methods=["GET"])
def getLastGasIncaData():
    """Lists all measurements of the gas inca table within the last hour - No parameters required"""
    try:
        final_timestamp_gases = datetime.datetime.now(dateutil.tz.tzutc())
        initial_timestamp_gases = final_timestamp_gases - datetime.timedelta(
            hours=1
        )
        gas_inca_last_data = get_data_helper.queryDBGasInca(
            initial_timestamp_gases, final_timestamp_gases
        )
        if gas_inca_last_data is not []:
            return make_response(jsonify(gas_inca_last_data), 200)
        return make_response(
            jsonify("We could not find any gas inca measurement"), 400
        )
    except Exception as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
