import datetime
from datetime import date, timedelta

import dateutil.parser
import dateutil.tz
import pytz
from flask import jsonify, make_response, request

import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.data.post_data_helper as post_data_helper
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, socketio

pollutants = ["CO", "CO2", "NO2", "O3", "H2S", "SO2", "PM25", "PM10", "VOC"]


@app.route("/api/processed_measurements/", methods=["GET"])
def getProcessedData():
    """Lists all measurements of processed measurement of the target qHAWAX within the initial and final date"""
    qhawax_name = request.args.get("name")
    try:
        interval_minutes = (
            int(request.args.get("interval_minutes"))
            if request.args.get("interval_minutes") is not None
            else 60
        )
        final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
        initial_timestamp = final_timestamp - datetime.timedelta(
            minutes=interval_minutes
        )
        processed_measurements = get_data_helper.queryDBProcessed(
            qhawax_name, initial_timestamp, final_timestamp
        )
        if processed_measurements is not None:
            return make_response(jsonify(processed_measurements), 200)
        return make_response(jsonify("Measurements not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


# @app.route('/api/dataProcessed/', methods=['POST'])
# def handleProcessedDataByQhawax():
#     """
#     Records processed and valid processed measurements every five seconds
#     qHAWAX: Record new measurement
#     """
#     flag_email = False
#     data_json = request.get_json()
#     try:
#         if (data_json is not None):
#             product_id = data_json['ID']
#             data_json = util_helper.validTimeJsonProcessed(data_json)
#             data_json = util_helper.validAndBeautyJsonProcessed(data_json)
#             post_data_helper.storeProcessedDataInDB(data_json) # it stores no matter the type
#             data_json['ID'] = product_id
#             data_json['zone'] = "Undefined Zone"
#             mode = same_helper.getQhawaxMode(product_id)
#             inca_value = same_helper.getMainIncaQhawaxTable(product_id)
#             type = same_helper.queryQhawaxType(product_id)
#             state = get_business_helper.queryQhawaxStatus(product_id)
#             # same endpoint for every qHAWAX but logic different per type of qHAWAX
#             if(type!=None):
#                 if(type == 'STATIC_EXT'):
#                     if(mode == "Customer" and inca_value!=None):
#                         data_json['zone'] = get_business_helper.getNoiseData(product_id)
#                         minutes_difference,last_time_turn_on = get_business_helper.getHoursDifference(product_id)
#                         if(minutes_difference!=None):
#                             if(minutes_difference<5):
#                                 post_data_helper.validTimeOfValidProcessed(10,"minute",last_time_turn_on,data_json,product_id,inca_value)
#                             elif(minutes_difference>=5):
#                                 post_data_helper.validTimeOfValidProcessed(2,"hour",last_time_turn_on,data_json,product_id,inca_value)
#                     data_json = util_helper.setNoneStringElements(data_json)
#                     socketio.emit(data_json['ID'] + '_processed', data_json)
#                     return make_response('OK', 200)
#                 elif(type == 'MOBILE_EXT'):
#                     if('zone' in data_json): data_json.pop('zone')
#                     #post_data_helper.storeProcessedDataInDB(data_json)
#                     if(state=='OFF'):
#                         post_business_helper.saveTurnOnLastTimeProcessedMobile(product_id)
#                         post_business_helper.saveStatusQhawaxTable(product_id,'ON',1)
#                         post_business_helper.writeBinnacle(product_id, "Reconnection", "API")

#                     if(mode == "Customer"):
#                         minutes_difference,last_time_turn_on = get_business_helper.getHoursDifference(product_id)
#                         if(minutes_difference!=None): # either one of these
#                             if(minutes_difference<30):
#                                 if(last_time_turn_on + datetime.timedelta(minutes=5)< datetime.datetime.now(dateutil.tz.tzutc())):
#                                     if(not(same_helper.isMobileQhawaxInATrip(product_id))):
#                                         post_data_helper.recordStartTrip(product_id)
#                                     post_data_helper.validAndBeautyJsonValidProcessedMobile(data_json,product_id) # socket emit

#                             elif(minutes_difference>=30):
#                                 if(last_time_turn_on + datetime.timedelta(hours=2) < datetime.datetime.now(dateutil.tz.tzutc())):
#                                     if(not(same_helper.isMobileQhawaxInATrip(product_id))): #in case trip has finished, a new one has to begin...
#                                         post_data_helper.recordStartTrip(product_id)
#                                     post_data_helper.validAndBeautyJsonValidProcessedMobile(data_json,product_id) # socket emit

#                     return make_response('OK', 200)
#                 elif(type == 'AEREAL'):
#                     if(mode == "Customer" and inca_value!=None):
#                         data_json['zone'] = get_business_helper.getNoiseData(product_id)
#                         minutes_difference,last_time_turn_on = get_business_helper.getHoursDifference(product_id)
#                         if(minutes_difference!=None):
#                             if(minutes_difference<5):
#                                 post_data_helper.validTimeOfValidProcessed(10,"minute",last_time_turn_on,data_json,product_id,inca_value)
#                             elif(minutes_difference>=5):
#                                 post_data_helper.validTimeOfValidProcessed(2,"hour",last_time_turn_on,data_json,product_id,inca_value)
#                     data_json = util_helper.setNoneStringElements(data_json)
#                     socketio.emit(data_json['ID'] + '_processed', data_json)
#                     return make_response('OK', 200)
#                 else:
#                     return make_response('qHAWAX type not supported', 200)
#             else:
#                 return make_response('qHAWAX type not defined', 200)

#     except TypeError as e:
#         json_message = jsonify({'error': '\'%s\'' % (e)})
#         return make_response(json_message, 400)


@app.route("/api/dataProcessed/", methods=["POST"])
def handleProcessedDataByQhawax():
    """
    Records processed and valid processed measurements every five seconds
    qHAWAX: Record new measurement
    """
    flag_email = False
    data_json = request.get_json()
    try:
        product_id = data_json["ID"]
        data_json = util_helper.validTimeJsonProcessed(data_json)
        data_json = util_helper.validAndBeautyJsonProcessed(data_json)
        post_data_helper.storeProcessedDataInDB(data_json)
        data_json["ID"] = product_id
        data_json["zone"] = "Undefined Zone"
        mode = same_helper.getQhawaxMode(product_id)
        inca_value = same_helper.getMainIncaQhawaxTable(product_id)
        # same endpoint for every qHAWAX but logic different per type of qHAWAX
        if mode == "Customer" and inca_value != None:
            data_json["zone"] = get_business_helper.getNoiseData(product_id)
            (
                minutes_difference,
                last_time_turn_on,
            ) = get_business_helper.getHoursDifference(product_id)
            if minutes_difference != None:
                if minutes_difference < 5:
                    post_data_helper.validTimeOfValidProcessed(
                        10,
                        "minute",
                        last_time_turn_on,
                        data_json,
                        product_id,
                        inca_value,
                    )
                elif minutes_difference >= 5:
                    post_data_helper.validTimeOfValidProcessed(
                        2,
                        "hour",
                        last_time_turn_on,
                        data_json,
                        product_id,
                        inca_value,
                    )
        data_json = util_helper.setNoneStringElements(data_json)
        socketio.emit(data_json["ID"] + "_processed", data_json)
        return make_response("OK", 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/dataProcessedMobile/", methods=["POST"])
def handleProcessedDataByMobileQhawax():
    data_json = request.get_json()
    try:
        product_id = data_json["ID"]
        if data_json is not None:
            if "zone" in data_json:
                data_json.pop("zone")
            post_data_helper.storeProcessedDataInDB(data_json)
            data_json["ID"] = product_id
            state = get_business_helper.queryQhawaxStatus(product_id)
            mode = same_helper.getQhawaxMode(product_id)
            if state == "OFF":  # if API turned it off
                post_business_helper.saveTurnOnLastTimeProcessedMobile(
                    product_id
                )
                post_business_helper.saveStatusQhawaxTable(
                    product_id, "ON", 1
                )  # state = ON - qhawax
                post_business_helper.writeBinnacle(
                    product_id, "Reconnection", "API"
                )

            if mode == "Customer":
                (
                    minutes_difference,
                    last_time_turn_on,
                ) = get_business_helper.getHoursDifference(product_id)
                if minutes_difference != None:
                    if minutes_difference < 30:
                        if last_time_turn_on + datetime.timedelta(
                            minutes=1
                        ) < datetime.datetime.now(dateutil.tz.tzutc()):
                            post_data_helper.validAndBeautyJsonValidProcessedMobile(
                                data_json, product_id
                            )

                    elif minutes_difference >= 30:
                        if last_time_turn_on + datetime.timedelta(
                            hours=2
                        ) < datetime.datetime.now(dateutil.tz.tzutc()):
                            post_data_helper.validAndBeautyJsonValidProcessedMobile(
                                data_json, product_id
                            )

            return make_response("OK", 200)
        return make_response("ID not found", 400)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/dataProcessedDrone/", methods=["POST"])
def handleProcessedDataByDrone():
    """
    Records processed and valid processed measurements every second by drone
    qHAWAX: Record new measurement
    """
    flag_email = False
    data_json = request.get_json()
    try:
        product_id = data_json["ID"]
        data_json = util_helper.validTimeJsonProcessed(data_json)
        data_json = util_helper.validAndBeautyJsonProcessed(data_json)
        post_data_helper.storeProcessedDataInDB(data_json)
        data_json["ID"] = product_id
        data_json = util_helper.setNoneStringElements(data_json)
        for i in range(len(pollutants)):
            socket_name = (
                data_json["ID"] + "_" + str(pollutants[i]) + "_processed"
            )
            pollutant = (
                str(pollutants[i]) + "_ug_m3"
                if (pollutants[i] in ["CO", "NO2", "O3", "H2S", "SO2"])
                else str(pollutants[i])
            )
            new_data_json = {
                "sensor": pollutants[i],
                "center": {"lat": data_json["lat"], "lng": data_json["lon"]},
            }
            new_data_json[pollutants[i]] = data_json[pollutant]
            socketio.emit(socket_name, new_data_json)  # qH006_CO_proccessed
        return make_response("OK", 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/processed_measurements_andean_drone/", methods=["GET"])
def getProcessedDataFromAndeanDrone():
    """Lists all measurements of processed measurement of the target drone within the initial and final date"""
    json_message, status = _getProcessedDataCommon(is_valid=False)
    return make_response(json_message, status) 


@app.route("/api/measurements_by_pollutant_during_flight/", methods=["GET"])
def getProcessedByPollutantDuringFlight():
    """Lists all measurements of processed measurement of the target qHAWAX within the initial and final date"""
    qhawax_name = str(request.args.get("name"))
    pollutant = str(request.args.get("pollutant"))
    try:
        start_flight = get_data_helper.qHAWAXIsInFlight(qhawax_name)
        if start_flight is not None:
            final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
            processed_measurements = (
                get_data_helper.queryDBProcessedByPollutant(
                    qhawax_name, start_flight, final_timestamp, pollutant
                )
            )
            if processed_measurements is not None:
                return make_response(jsonify(processed_measurements), 200)
        return make_response(jsonify("Measurements not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/processed_measurements_before_48_hours/", methods=["POST"])
def deleteProcessedMeasurementsBefore48Hours():
    # qhawax_name = str(request.args.get('qhawax_name'))
    try:
        before = datetime.datetime.now(
            dateutil.tz.tzutc()
        ) - datetime.timedelta(hours=48)
        # qhawax_id = same_helper.getQhawaxID(qhawax_name)
        data = (
            post_data_helper.deleteValuesBetweenTimestampsProcessedMeasurement(
                before
            )
        )
        if data is not None:
            return make_response(jsonify(data), 200)
        return make_response(jsonify("Measurements not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route(
    "/api/valid_processed_measurements_before_48_hours/", methods=["POST"]
)
def deleteValidProcessedMeasurementsBefore48Hours():
    # qhawax_name = str(request.args.get('qhawax_name'))
    try:
        before = datetime.datetime.now(
            dateutil.tz.tzutc()
        ) - datetime.timedelta(hours=48)
        # qhawax_id = same_helper.getQhawaxID(qhawax_name)
        data = post_data_helper.deleteValuesBetweenTimestampsValidProcessedMeasurement(
            before
        )
        if data is not None:
            return make_response(jsonify(data), 200)
        return make_response(jsonify("Measurements not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/processed_measurements_mobile_qhawax/", methods=["GET"])
def getProcessedDataFromMobileQhawax():
    """Lists all measurements of processed measurement of the target drone within the initial and final date"""
    json_message, status = _getProcessedDataCommon(is_valid=False)
    return make_response(json_message, status)
    

@app.route("/api/valid_processed_measurements_mobile_qhawax/", methods=["GET"])
def getValidProcessedDataFromMobileQhawax():
    """Lists all measurements of processed measurement of the target drone within the initial and final date"""
    json_message, status = _getProcessedDataCommon(is_valid=True)
    return make_response(json_message, status)
    
    
@app.route("/api/measurements_by_pollutant_during_trip/", methods=["GET"])
def getProcessedByPollutantDuringTrip():
    """Lists all measurements of processed measurement of the target qHAWAX within the initial and final date"""
    qhawax_name = str(request.args.get("name"))
    pollutant = str(request.args.get("pollutant"))
    try:
        start_trip = get_data_helper.qHAWAXIsInTrip(qhawax_name)
        if start_trip is not None:
            final_timestamp = datetime.datetime.now(dateutil.tz.tzutc())
            # verify which sensors
            processed_measurements = (
                get_data_helper.queryDBValidProcessedByPollutantMobile(
                    qhawax_name, start_trip, final_timestamp, pollutant
                )
            )
            if processed_measurements is not None:
                return make_response(jsonify(processed_measurements), 200)
        return make_response(jsonify("Measurements not found"), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/function_testers/", methods=["GET"])
def testerFunction():
    try:
        qhawax_name = "qH022"
        val = get_data_helper.getqHAWAXMobileLatestTripStart(qhawax_name)
        # post_business_helper.saveTurnOnLastTime(qhawax_name)
        # start_trip = datetime.datetime.now()
        # get_business_helper.getHoursDifference(qhawax_name)
        # post_data_helper.recordStartTrip(qhawax_name)
        # jsonLatLon = get_data_helper.getMobileLatestLatLonValidProcessedMeasurement(qhawax_name)
        # post_data_helper.updateLastestLatLonMobile(qhawax_name,jsonLatLon)
        # return make_response(jsonify(jsonLatLon), 200)
        return make_response(str(val), 200)
    except Exception as e:
        json_message = jsonify({"error": " '%s' " % (e)})
        return make_response(json_message, 400)

# Helper/Private functions
def _getProcessedDataCommon(is_valid):
    """ Returns a json that lists all measurements of processed measurement 
    of the target drone within the initial and final date """

    qhawax_name = request.args.get('qhawax_name')
    initial_timestamp = datetime.datetime.strptime(request.args.get('initial_timestamp'), '%d-%m-%Y %H:%M:%S')
    final_timestamp = datetime.datetime.strptime(request.args.get('final_timestamp'), '%d-%m-%Y %H:%M:%S')
    try:
        processed_measurements = None
        if is_valid:
            processed_measurements = get_data_helper.queryDBValidProcessed(qhawax_name, initial_timestamp, final_timestamp)
        else:
            processed_measurements = get_data_helper.queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp)
        if processed_measurements is not None:
            return jsonify(processed_measurements), 200
        return jsonify('Measurements not found'), 200
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return json_message, 400
