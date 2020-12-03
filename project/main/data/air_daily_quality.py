from flask import jsonify, make_response, request
from project import app, db, socketio
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper

@app.route('/api/air_daily_quality_measurements/', methods=['POST'])
def storeAirDailyData():
    """
    Air Daily Measurement function to record daily average measurement 
    """
    data_json = request.get_json()
    try:
        #falta colocar exception del formato json
        post_data_helper.storeAirDailyQualityDataInDB(data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/air_daily_measurements_period/', methods=['GET'])
def getAirDailyMeasurementsTimePeriod():
    """
    Air Daily Measurement function to get daily average measurement based on week number and year 
    """
    qhawax_id = int(request.args.get('qhawax_id')) if request.args.get('qhawax_id') is not None else 0 
    init_week = int(request.args.get('init_week')) if request.args.get('init_week') is not None else 30 
    init_year = int(request.args.get('init_year')) if request.args.get('init_year') is not None else 2020 
    end_week  = int(request.args.get('end_week')) if request.args.get('end_week') is not None else 35 
    end_year  = int(request.args.get('end_year')) if request.args.get('end_year') is not None else 2020 
    try:
        air_daily_measurements = get_data_helper.queryDBAirDailyQuality(qhawax_id, init_week, \
                                                                        init_year, end_week, end_year)
        if air_daily_measurements is not None:
            return make_response(jsonify(air_daily_measurements), 200)
        return make_response(jsonify('Measurements not found'), 200)
    except (TypeError,ValueError) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
