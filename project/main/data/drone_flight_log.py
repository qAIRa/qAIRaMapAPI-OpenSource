import project.main.business.post_business_helper as post_business_helper
import project.main.business.get_business_helper as get_business_helper
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.exceptions as exception_helper
from flask import jsonify, make_response, request
from datetime import timedelta
from project import app
import dateutil.parser
import dateutil.tz
import datetime

@app.route('/api/record_start_flight/', methods=['POST'])
def recordDroneTakeoff():
    req_json = request.get_json()
    try:
        flight_start, qhawax_name = exception_helper.getJsonOfTakeOff(req_json)
        if(get_business_helper.isAerealQhawax(qhawax_name)==True):
            post_data_helper.recordDroneTakeoff(flight_start, qhawax_name)
            return make_response({'Success':'The drone takeoff has been recorded'}, 200)
        return make_response({'Warning':'This is not an andean drone'}, 400)
    except (TypeError, ValueError ) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/complete_flight/', methods=['POST'])
def recordDroneLanding():
    req_json = request.get_json()
    try:
        flight_end, qhawax_name,flight_detail,location = exception_helper.getJsonOfLanding(req_json)
        if(get_business_helper.isAerealQhawax(qhawax_name)==True):
            post_data_helper.recordDroneLanding(flight_end, qhawax_name,flight_detail)
            post_business_helper.updateLastLocation(qhawax_name,location)
            return make_response({'Success':'The drone landing has been recorded'}, 200)
        return make_response({'Warning':'This is not an andean drone'}, 400)
    except (TypeError, ValueError ) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_drone_flights_period_time/', methods=['GET'])
def getDroneFlightDuringPeriodTime():
    """ To list all flights during the certain period of time """
    initial_timestamp = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
    final_timestamp = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')
    try:
        flights = get_data_helper.queryFlightsFilterByTime(initial_timestamp, final_timestamp)
        return make_response(jsonify(flights), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)