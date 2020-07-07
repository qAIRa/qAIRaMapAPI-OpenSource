from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
import project.main.data.data_helper as helper


@app.route('/api/air_daily_quality_measurements/', methods=['POST'])
def storeAirDailyData():
    try:
        data_json = request.get_json()
        helper.storeAirDailyQualityDataInDB(data_json)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format. Exception="%s"' % (e), 400)