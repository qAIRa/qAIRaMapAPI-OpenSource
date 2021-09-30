from flask import jsonify, make_response, request

import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.exceptions as exception_helper
import project.main.same_function_helper as same_helper
from project import app


@app.route("/api/AllQhawaxInMap/", methods=["GET"])
def getQhawaxInMap():
    """Gets a list of qHAWAXs filter by company ID"""
    try:
        qhawax_in_field = get_business_helper.queryQhawaxTypeInFieldInPublicMode('STATIC_EXT')
        return make_response(jsonify(qhawax_in_field), 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/AllDronesInMap/", methods=["GET"])
def getDronesInMap():
    """Gets a list of qHAWAXs filter by company ID"""
    try:
        drones_in_field = (
            get_business_helper.queryQhawaxTypeInFieldInPublicMode("AEREAL")
        )
        if drones_in_field != []:
            return make_response(jsonify(drones_in_field), 200)
        return make_response(
            jsonify({"Warning": "Drones in field not found"}), 400
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/AllMobileQhawaxsInMap/", methods=["GET"])
def getMobileQhawaxsInMap():
    """Gets a list of qHAWAXs filter by company ID"""
    try:
        mobile_qH_in_map = (
            get_business_helper.queryQhawaxTypeInFieldInPublicMode(
                "MOBILE_EXT"
            )
        )
        if mobile_qH_in_map != []:
            return make_response(jsonify(mobile_qH_in_map), 200)
        return make_response(
            jsonify({"Warning": "Mobiles in field not found"}), 200
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/GetInstallationDate/", methods=["GET"])
def getInstallationDate():
    """Gets the installation date of qHAWAX in field"""
    qhawax_id = int(request.args.get("qhawax_id"))
    try:
        installation_date = get_business_helper.getInstallationDate(qhawax_id)
        first_timestamp = get_data_helper.getFirstTimestampValidProcessed(
            qhawax_id
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
    else:
        if installation_date == None:
            return make_response(
                {
                    "Warning ": "qHAWAX ID "
                    + str(qhawax_id)
                    + " has not been found in field"
                },
                400,
            )
        if first_timestamp > installation_date:
            return str(first_timestamp)
        return str(installation_date)


@app.route("/api/newQhawaxInstallation/", methods=["POST"])
def newQhawaxInstallation():
    """Creates a qHAWAX in Field"""
    data_json = request.get_json()
    description = "qHAWAX was recorded in field"
    try:
        qH_name, in_charge = exception_helper.getInstallationFields(data_json)
        post_business_helper.storeNewQhawaxInstallation(data_json)
        post_business_helper.util_qhawax_installation_set_up(
            qH_name, "Occupied", "Customer", description, in_charge
        )
        return make_response({"Success": "Save new qHAWAX in field"}, 200)
    except Exception as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/saveEndWorkField/", methods=["POST"])
def saveEndWorkField():
    """Saves the last date of qHAWAX in field"""
    data_json = request.get_json()
    description = "qHAWAX has finished work in field"
    try:
        (
            qH_name,
            end_date,
            person_in_charge,
        ) = exception_helper.validEndWorkFieldJson(data_json)
        post_business_helper.saveEndWorkFieldDate(qH_name, end_date)
        mode = (
            "Stand By"
            if (same_helper.getQhawaxMode(qH_name) == "Customer")
            else same_helper.getQhawaxMode(qH_name)
        )
        post_business_helper.util_qhawax_installation_set_up(
            qH_name, "Available", mode, description, person_in_charge
        )
        return make_response("Success: Save last day in field", 200)
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)


@app.route("/api/updateQhawaxInstallation/", methods=["POST"])
def updateQhawaxInstallation():
    """Updates qHAWAX in Field"""
    data_json = request.get_json()
    description = "Some fields of qHAWAX installation were updated"
    try:
        qH_name, in_charge = exception_helper.getInstallationFields(data_json)
        post_business_helper.updateQhawaxInstallation(data_json)
        post_business_helper.writeBinnacle(qH_name, description, in_charge)
        return make_response(
            {"Sucess": "qHAWAX field information have been updated"}, 200
        )
    except TypeError as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
