from flask import jsonify, make_response, request
import datetime
from project import app
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper

@app.route('/api/air_quality_measurements/', methods=['POST'])
def storeAirQualityData():
    """
    POST: To record processed measurement and valid processed measurement every five seconds

    """
    try:
        data_json = request.get_json()
        post_data_helper.storeAirQualityDataInDB(data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/air_quality_measurements_period/', methods=['GET'])
def getAirQualityMeasurementsTimePeriod():
    """
    To list all measurement in ppb of air quality measurement table in a define period of time
    This is an hourly average measurement

    """
    qhawax_name = str(request.args.get('name'))
    initial_timestamp_utc = str(request.args.get('initial_timestamp'))
    final_timestamp_utc = str(request.args.get('final_timestamp'))
    try:
        date_format = '%d-%m-%Y %H:%M:%S'
        air_quality_measurements = get_data_helper.queryDBAirQuality(qhawax_name, initial_timestamp_utc, \
                                                                     final_timestamp_utc,date_format)
        if air_quality_measurements is not None:
            return make_response(jsonify(air_quality_measurements), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/gas_average_measurement/', methods=['GET'])
def getGasAverageMeasurementsEvery24():
    """
    To list all values by a define gas or dust in ug/m3 of air quality measurement table of the last 24 hours

    """
    try:
        qhawax_name = request.args.get('qhawax')
        gas_name = request.args.get('gas')
        gas_average_measurement = get_data_helper.queryDBGasAverageMeasurement(qhawax_name, gas_name)
        gas_average_measurement_list = util_helper.getFormatData(gas_average_measurement)
        if(gas_average_measurement_list is not None):
            return make_response(jsonify(gas_average_measurement_list), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except (ValueError,TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/average_valid_processed_period/', methods=['GET'])
def getAverageValidProcessedMeasurementsTimePeriod():
    """
    To list all average measurement of valid processed measurement table in a define period of time and company
    """
    qhawax_id = int(request.args.get('qhawax_id'))
    initial_timestamp = str(request.args.get('initial_timestamp'))
    final_timestamp = str(request.args.get('final_timestamp'))
    try:
        date_format = '%d-%m-%Y %H:%M:%S'
        average_valid_processed_measurements = get_data_helper.queryDBValidAirQuality(qhawax_id, initial_timestamp,\
                                                                                     final_timestamp, date_format)
        if average_valid_processed_measurements is not None:
            return make_response(jsonify(average_valid_processed_measurements), 200)
        return make_response(jsonify('Valid Measurements not found'), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)





