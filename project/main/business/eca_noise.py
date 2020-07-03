from flask import jsonify, make_response, request

from project import app, db, socketio
from project.database.models import EcaNoise
import project.main.business.business_helper as helper

@app.route('/api/get_eca_noise_limit/', methods=['GET'])
def getEcaNoiseLimitById():
    """
    To get eca noise minimun and maximun

    :type ID: string
    :param ID: Eca Noise ID

    """
    noiseID = request.args.get('ID')
    if(noiseID!=None):
        ecaNoiseInfo = helper.queryGetEcaNoise(noiseID)
        if ecaNoiseInfo is not None:
            return make_response(jsonify(ecaNoiseInfo), 200)
    return make_response(jsonify('Eca noise not found'), 404)

@app.route('/api/get_all_areas/', methods=['GET'])
def getAllAreas():
    """
    To list all areas in a combo box

    No parameters required

    """
    allAreas = helper.queryGetAreas()
    if allAreas is not None:
        allAreas_list = [{'area_name': area.area_name, 'id': area.id} for area in allAreas]
        return make_response(jsonify(allAreas_list), 200)
    return make_response(jsonify('Areas not found'), 404)


