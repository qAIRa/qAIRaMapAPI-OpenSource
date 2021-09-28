import datetime
from datetime import timedelta

import dateutil.parser
import dateutil.tz
from flask import jsonify, make_response, request

import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
import project.main.exceptions as exception_helper
from project import app, socketio


@app.route("/api/record_start_flight/", methods=["POST"])
def recordDroneTakeoff():
    req_json = request.get_json()
    try:
        flight_start, qhawax_name = exception_helper.getJsonOfTakeOff(req_json)
        if get_business_helper.isAerealQhawax(qhawax_name) == True:
            post_data_helper.recordDroneTakeoff(flight_start, qhawax_name)
            socketio.emit(qhawax_name + "_takeoff", flight_start)
            return make_response(
                {"Success": "The drone takeoff has been recorded"}, 200
            )
        return make_response({"Warning": "This is not an andean drone"}, 400)
    except (TypeError, ValueError) as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({"database error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/complete_flight/", methods=["POST"])
def recordDroneLanding():
    req_json = request.get_json()
    try:
        (
            flight_end,
            qhawax_name,
            flight_detail,
            location,
        ) = exception_helper.getJsonOfLanding(req_json)
        if get_business_helper.isAerealQhawax(qhawax_name) == True:
            post_data_helper.recordDroneLanding(
                flight_end, qhawax_name, flight_detail
            )
            post_business_helper.updateLastLocation(qhawax_name, location)
            socketio.emit(
                qhawax_name + "_landing", flight_end
            )  # insert qhawax_name
            return make_response(
                {"Success": "The drone landing has been recorded"}, 200
            )
        return make_response({"Warning": "This is not an andean drone"}, 400)
    except (TypeError, ValueError) as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({"database error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/get_drone_flights_period_time/", methods=["GET"])
def getDroneFlightDuringPeriodTime():
    """To list all flights during the certain period of time"""
    initial_timestamp = datetime.datetime.strptime(
        request.args.get("initial_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    final_timestamp = datetime.datetime.strptime(
        request.args.get("final_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    try:
        flights = get_data_helper.queryFlightsFilterByTime(
            initial_timestamp, final_timestamp
        )
        return make_response(jsonify(flights), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/get_mobile_trips_period_time/", methods=["GET"])
def getMobileTripPeriodTime():
    """To list all flights during the certain period of time"""
    initial_timestamp = datetime.datetime.strptime(
        request.args.get("initial_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    final_timestamp = datetime.datetime.strptime(
        request.args.get("final_timestamp"), "%d-%m-%Y %H:%M:%S"
    )
    try:
        trips = get_data_helper.queryMobileTripsByTimestamp(
            initial_timestamp, final_timestamp
        )
        return make_response(jsonify(trips), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/flight_log_info_by_qhawax_name/", methods=["GET"])
def getFlightLogInfoByQhawaxName():
    """Lists all measurements of processed measurement of the target qHAWAX within the initial and final date"""
    qhawax_name = str(request.args.get("name"))
    try:
        start_flight = get_data_helper.qHAWAXIsInFlight(qhawax_name)
        if start_flight is not None:
            json = {"start_flight": start_flight, "qhawax_name": qhawax_name}
            return make_response(jsonify(json), 200)
        return make_response(
            jsonify("qHAWAX " + str(qhawax_name) + " is not in flight"), 200
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/flight_log_info_during_flight/", methods=["GET"])
def getFlightLogDuringFlight():
    """Lists all measurements of processed measurement of the target qHAWAX within the initial and final date"""
    try:
        allQhawaxsInFlight = get_data_helper.AllqHAWAXIsInFlight()
        if allQhawaxsInFlight != []:
            return make_response(jsonify(allQhawaxsInFlight), 200)
        return make_response(jsonify("There are no qHAWAXs in flight"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/mobile_log_info_during_trip/", methods=["GET"])
def getMobileLogDuringTrip():
    """Lists all trips"""
    try:
        allQhawaxsInFlight = get_data_helper.AllqHAWAXIsInTrip()
        if allQhawaxsInFlight != []:
            return make_response(jsonify(allQhawaxsInFlight), 200)
        return make_response(jsonify("There are no qHAWAXs in a trip"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/mobile_log_info_by_qhawax_name/", methods=["GET"])
def getMobileLogInfoByQhawaxName():
    qhawax_name = str(request.args.get("name"))
    try:
        start_trip = get_data_helper.qHAWAXIsInTrip(qhawax_name)
        if start_trip is not None:
            json = {"start_trip": start_trip, "qhawax_name": qhawax_name}
            return make_response(jsonify(json), 200)
        return make_response(
            jsonify("qHAWAX " + str(qhawax_name) + " is not in trip"), 200
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/mobile_log_info_by_qhawax_name_turn_and_id/", methods=["GET"])
def getMobileLogAndTurnsByQhawaxName():
    qhawax_name = str(request.args.get("name"))
    turn = int(request.args.get("turn"))
    id = int(request.args.get("id"))
    try:
        if turn not in [1, 2, 3, 4]:
            return make_response(jsonify("Incorrect turn"), 200)
        else:
            trip_data = get_data_helper.getqHAWAXMobileTripByTurn(
                qhawax_name, turn, id
            )
            if trip_data is not None:
                return make_response(jsonify(trip_data), 200)
        return make_response(
            jsonify(
                "qHAWAX "
                + str(qhawax_name)
                + " does not have available data for the specified parameters"
            ),
            200,
        )
    except Exception as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
