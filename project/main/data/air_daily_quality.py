from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
from project import app, db, socketio
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper


@app.route('/api/air_daily_quality_measurements/', methods=['POST'])
def storeAirDailyData():
    """
    Air Daily Measurement function to record daily average measurement 

    :type data_json: json
    :param data_json: json of daily average measurement

    """
    try:
        data_json = request.get_json()
        post_data_helper.storeAirDailyQualityDataInDB(data_json)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format. Exception="%s"' % (e), 400)

@app.route('/api/air_daily_measurements_period/', methods=['GET'])
def getAirDailyMeasurementsTimePeriod():
    """
    Air Daily Measurement function to get daily average measurement based on week number and year 

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type init_week: integer
    :param init_week: initial week number

    :type init_year: integer
    :param init_year: initial year

    :type end_week: integer
    :param end_week: last week number

    :type end_year: integer
    :param end_year: end year

    """
    qhawax_id = int(request.args.get('qhawax_id'))
    init_week = int(request.args.get('init_week'))
    init_year = int(request.args.get('init_year'))
    end_week = int(request.args.get('end_week'))
    end_year = int(request.args.get('end_year'))

    air_daily_measurements = get_data_helper.queryDBAirDailyQuality(qhawax_id, init_week, init_year,end_week, end_year)
    if air_daily_measurements is not None:
        air_quality_measurements_list = [measurement._asdict() for measurement in air_daily_measurements]
        return make_response(jsonify(air_quality_measurements_list), 200)
    else:
        return make_response(jsonify('Measurements not found'), 404)
