from flask import jsonify, make_response, request
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper
from project import app
import datetime

@app.route('/api/air_quality_measurements/', methods=['POST'])
def storeAirQualityData():
    """ POST: To record processed measurement and valid processed measurement every five seconds """
    data_json = request.get_json()
    try:
        #revisar el json con un exception
        post_data_helper.storeAirQualityDataInDB(data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/air_quality_measurements_period/', methods=['GET'])
def getAirQualityMeasurementsTimePeriod():
    """ To list all measurement in ppb of air quality measurement table in a define period of time
        This is an hourly average measurement """
    qhawax_name = str(request.args.get('name'))
    initial_timestamp_utc = str(request.args.get('initial_timestamp'))
    final_timestamp_utc = str(request.args.get('final_timestamp'))
    try:
        date_format = '%Y-%m-%d %H:%M:%S'
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
    """ To list all values by a define gas or dust in ug/m3 of air quality measurement table of the last 24 hours """
    qhawax_name = str(request.args.get('qhawax'))
    gas_name = str(request.args.get('gas'))
    try:
        gas_average_measurement = get_data_helper.queryDBGasAverageMeasurement(qhawax_name, gas_name)
        gas_average_measurement_list = util_helper.getFormatData(gas_average_measurement)
        if(gas_average_measurement_list is not None):
            return make_response(jsonify(gas_average_measurement_list), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except (ValueError,TypeError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/average_valid_processed_period/', methods=['GET'])
def getAverageValidProcessedMeasurementsTimePeriodByCompany():
    """ To list all average measurement of valid processed measurement table in a define period of time and company """
    try:
        qhawax_id = int(request.args.get('qhawax_id'))
        initial_timestamp = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
        final_timestamp = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')

        average_valid_processed_measurements = get_data_helper.queryDBValidAirQuality(qhawax_id, initial_timestamp, final_timestamp)
        average_valid_processed_measurements_list = [measurement._asdict() for measurement in average_valid_processed_measurements]
        return make_response(jsonify(average_valid_processed_measurements_list), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/measurementPromedio/', methods=['GET'])
def requestProm():
    """ get average of determine pollutant (CO,H2S,NO2,O3,PM10,PM25,SO2) """
    name = request.args.get('name')
    sensor = request.args.get('sensor')
    hoursSensor = request.args.get('hoursSensor')
    minutes_diff = int(request.args.get('minutes_diff'))
    qhawax_measurement_sensor=-1
    try:
        if(minutes_diff<5):
            last_time_turn_on = dateutil.parser.parse(request.args.get('last_time_turn_on')) + datetime.timedelta(minutes=10)
        elif(minutes_diff>=5):
            last_time_turn_on = dateutil.parser.parse(request.args.get('last_time_turn_on')) + datetime.timedelta(hours=2)
        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
        initial_timestamp = final_timestamp - datetime.timedelta(hours=int(hoursSensor))
        if(initial_timestamp.replace(tzinfo=None)>=last_time_turn_on.replace(tzinfo=None)):
            qhawax_measurement_sensor = get_data_helper.queryDBPROM(name, sensor, initial_timestamp, final_timestamp)
        return str(qhawax_measurement_sensor)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
