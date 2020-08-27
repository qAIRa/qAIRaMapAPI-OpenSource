from flask import jsonify, make_response, request
from project.database.models import EcaNoise
import project.main.business.get_business_helper as get_business_helper
from project import app

@app.route('/api/get_eca_noise_limit/', methods=['GET'])
def getEcaNoiseLimitById():
    """
    To get eca noise minimun and maximun

    :type ID: string
    :param ID: Eca Noise ID

    """
    try:
        noiseID = int(request.args.get('ID'))
        ecaNoiseInfo = get_business_helper.queryGetEcaNoise(noiseID)
        if ecaNoiseInfo is not None:
            return make_response(jsonify(ecaNoiseInfo), 200)
        else:
            return make_response(jsonify({'Warning':'Eca noise ID has not been found'}), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

@app.route('/api/get_all_areas/', methods=['GET'])
def getAllAreas():
    """
    To list all areas in a combo box

    No parameters required

    """
    try:
        allAreas = get_business_helper.queryGetAreas()
        if allAreas is not None:
            allAreas_list = [{'area_name': area.area_name, 'id': area.id} for area in allAreas]
            return make_response(jsonify(allAreas_list), 200)
        return make_response(jsonify({'Warning':'There are no areas recorded in database'}), 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)