import datetime

from flask import jsonify, make_response, request

import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
import project.main.util_helper as util_helper
from project import app


@app.route("/api/air_quality_measurements/", methods=["POST"])
def storeAirQualityData():
    """POST: Records processed and valid processed measurements every five seconds"""
    data_json = request.get_json()
    try:
        post_data_helper.storeAirQualityDataInDB(data_json)
        return make_response("OK", 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/average_valid_processed_period/", methods=["GET"])
def getAverageValidProcessedMeasurementsTimePeriod():
    """Lists all average measurements of valid processed measurement table in a defined period of time and company"""
    try:
        qhawax_id = int(request.args.get("qhawax_id"))
        initial_timestamp = datetime.datetime.strptime(
            request.args.get("initial_timestamp"), "%d-%m-%Y %H:%M:%S"
        )
        final_timestamp = datetime.datetime.strptime(
            request.args.get("final_timestamp"), "%d-%m-%Y %H:%M:%S"
        )
        average_valid_processed_measurements = (
            get_data_helper.queryDBValidAirQuality(
                qhawax_id, initial_timestamp, final_timestamp
            )
        )
        if average_valid_processed_measurements not in [[], None]:
            return make_response(
                jsonify(average_valid_processed_measurements), 200
            )
        return make_response(jsonify("Measurements not found"), 400)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/gas_average_measurement/", methods=["GET"])
def getGasAverageMeasurementsEvery24():
    """Lists all values by a defined gas or dust in ug/m3 of air quality measurement table of the last 24 hours"""
    qhawax_name = str(request.args.get("qhawax"))
    gas_name = str(request.args.get("gas"))
    try:
        gas_average_measurement = get_data_helper.queryDBGasAverageMeasurement(
            qhawax_name, gas_name
        )
        gas_average_measurement_list = util_helper.getFormatData(
            gas_average_measurement
        )
        if gas_average_measurement_list is not None:
            return make_response(jsonify(gas_average_measurement_list), 200)
        return make_response(jsonify("Measurements not found"), 400)
    except (ValueError, TypeError) as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
