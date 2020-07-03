from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
import os

from project import app, db, socketio
from project.database.models import EcaNoise
import project.main.data.data_helper as helper
from sqlalchemy import or_

@app.route('/api/saveGasInca/', methods=['POST'])
def handleGasInca():
    try:
        data_json = request.get_json()
        helper.storeGasIncaInDB(data_json)
        socketio.emit('gas_inca_summary', data_json)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/last_gas_inca_data/', methods=['GET'])
def getLastGasIncaData():
    final_timestamp_gases = datetime.datetime.now(dateutil.tz.tzutc()) - datetime.timedelta(hours=5)
    initial_timestamp_gases = final_timestamp_gases - datetime.timedelta(hours=1)
    gas_inca_last_data = helper.queryDBGasInca(initial_timestamp_gases, final_timestamp_gases)
    gas_inca_last_data_list = []
    if gas_inca_last_data is not None:  
        for measurement in gas_inca_last_data:
            measurement = measurement._asdict()
            measurement['qhawax_name'] = helper.getQhawaxName(measurement['qhawax_id'])[0]
            gas_inca_last_data_list.append(measurement)
        return make_response(jsonify(gas_inca_last_data_list), 200)
    else:
        return make_response(jsonify('Gas Inca not found'), 404)