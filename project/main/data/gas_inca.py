from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz
from project import app, db, socketio
import project.main.data.post_data_helper as post_data_helper
import project.main.data.get_data_helper as get_data_helper

@app.route('/api/saveGasInca/', methods=['POST'])
def handleGasInca():
    """
    POST: To record gas and dust measurement in gas inca table
    
    Json input of Air Quality Measurement

    Json input of Air Measurement

    :type timestamp_zone: string
    :param timestamp_zone: timestamp with time zone

    :type CO: double
    :param CO: value of CO measurement

    :type H2S: double
    :param H2S: value of H2S measurement

    :type SO2: double
    :param SO2: value of SO2 measurement

    :type NO2: double
    :param NO2: value of NO2 measurement

    :type O3: double
    :param O3: value of O3 measurement

    :type PM25: double
    :param PM25: value of PM25 measurement

    :type PM1: double
    :param PM1: value of PM1 measurement

    :type PM10: double
    :param PM10: value of PM10 measurement

    """
    try:
        data_json = request.get_json()
        post_data_helper.storeGasIncaInDB(data_json)
        socketio.emit('gas_inca_summary', data_json)
        return make_response('OK', 200)
    except Exception as e:
        print(e)
        return make_response('Invalid format', 400)

@app.route('/api/last_gas_inca_data/', methods=['GET'])
def getLastGasIncaData():
    """
    To list all measurement of the last hour from the gas inca table

    No parameters required

    """
    final_timestamp_gases = datetime.datetime.now(dateutil.tz.tzutc())
    initial_timestamp_gases = final_timestamp_gases - datetime.timedelta(hours=1)
    gas_inca_last_data = get_data_helper.queryDBGasInca(initial_timestamp_gases, final_timestamp_gases)
    gas_inca_last_data_list = []
    if gas_inca_last_data is not None:  
        for measurement in gas_inca_last_data:
            measurement = measurement._asdict()
            measurement['qhawax_name'] = get_data_helper.getQhawaxName(measurement['qhawax_id'])[0]
            gas_inca_last_data_list.append(measurement)
        return make_response(jsonify(gas_inca_last_data_list), 200)
    else:
        return make_response(jsonify('Gas Inca not found'), 404)