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
    noiseID = int(request.args.get('ID'))
    if(noiseID!=None):
        ecaNoiseInfo = helper.queryGetEcaNoise(noiseID)
        if ecaNoiseInfo is not None:
            return make_response(jsonify(ecaNoiseInfo), 200)
    return make_response(jsonify('Eca noise not found'), 404)



