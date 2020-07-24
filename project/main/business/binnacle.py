from flask import jsonify, make_response, request

from project import app
from project.database.models import Company
import project.main.business.business_helper as helper

@app.route('/api/get_all_observations_by_qhawax/', methods=['GET'])
def getAllObservationByQhawax():
    """
    To list all observations By qHAWAX

    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    """
    qhawax_id = request.args.get('qhawax_id')
    allObservations= helper.queryAllObservationByQhawax(qhawax_id)
    if allObservations is not None:
        allObservations_list = [observation._asdict() for observation in allObservations]
        return make_response(jsonify(allObservations_list), 200)
    return make_response(jsonify('Observations not found by this qHAWAX'), 404)

@app.route('/api/record_observation_binnacle/', methods=['POST'])
def insertObservation():
    """
    To record observations in field
    
    Json input of following fields:
    
    :type qhawax_id: integer
    :param qhawax_id: qHAWAX ID

    :type initial_timestamp: timestamp
    :param initial_timestamp: start observation

    :type end_timestamp: timestamp
    :param end_timestamp: end observation

    :type description: string
    :param description: description of the observation

    :type solution: string
    :param solution: solution of the observation

    :type person_in_charge: string
    :param person_in_charge: person in charge

    """
    try:
        req_json = request.get_json()
        helper.storeNewObservation(req_json)
        return make_response('Observation has been created', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)