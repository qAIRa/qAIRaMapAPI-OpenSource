from flask import jsonify, make_response, request
import datetime
import dateutil.parser
import dateutil.tz

from project import app, db, socketio
from project.database.models import Qhawax, ProcessedMeasurement
import project.main.data.data_helper as helper


@app.route('/api/valid_processed_measurements_period/', methods=['GET'])
def getValidProcessedMeasurementsTimePeriodByCompany():
    qhawax_id = request.args.get('qhawax_id')
    company_id = request.args.get('company_id')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    valid_processed_measurements=[]
    if(int(company_id)!=1):
        if (helper.qhawaxBelongsCompany(qhawax_id,company_id)):   
            installation_id = helper.getInstallationId(qhawax_id)
            valid_processed_measurements = helper.queryDBValidProcessedByQhawax(installation_id, initial_timestamp, final_timestamp)
    elif (int(company_id)==1):
        installation_id = helper.getInstallationId(qhawax_id)
        valid_processed_measurements = helper.queryDBValidProcessedByQhawax(installation_id, initial_timestamp, final_timestamp)
    if valid_processed_measurements is not None:
        valid_processed_measurements_list = [measurement._asdict() for measurement in valid_processed_measurements]
        return make_response(jsonify(valid_processed_measurements_list), 200)
    return make_response(jsonify('Valid Measurements not found'), 404)


@app.route('/api/valid_processed_measurements/', methods=['GET'])
def getValidProcessedData():
    qhawax_name = request.args.get('name')
    interval_minutes = int(request.args.get('interval_minutes')) \
        if request.args.get('interval_minutes') is not None else 60
    final_timestamp = datetime.datetime.now(dateutil.tz.tzutc()) - datetime.timedelta(hours=5)
    initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes)
    qhawax_id = db.session.query(Qhawax.id).filter_by(name=qhawax_name).first()[0]
    valid_processed_measurements={}
    
    if(qhawax_id!=None):
        installation_id = helper.getInstallationId(qhawax_id)
        valid_processed_measurements = helper.queryDBValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp)

    if valid_processed_measurements is not None:
        valid_processed_measurements_list = [valid_measurement._asdict() for valid_measurement in valid_processed_measurements]
        return make_response(jsonify(valid_processed_measurements_list), 200)
    else:
        return make_response(jsonify('Valid Measurements not found'), 404)

@app.route('/api/get_time_valid_data_active_qhawax/', methods=['GET'])
def getTimeOfValidProcessed():
    qhawax_name = request.args.get('name')
    return str(helper.getLatestTimestampValidProcessed(qhawax_name))

@app.route('/api/daily_valid_processed_measurements/', methods=['GET'])
def getDailyValidProcessedData():
    qhawax_id = request.args.get('id')
    final_timestamp = request.args.get('end_date')
    initial_timestamp = request.args.get('start_date')

    installation_id = helper.getInstallationId(qhawax_id)
    valid_processed_measurements = helper.queryDBDailyValidProcessedByQhawaxScript(installation_id, initial_timestamp, final_timestamp)

    if valid_processed_measurements is not None:
        valid_processed_measurements_list = [daily_valid_measurement._asdict() for daily_valid_measurement in valid_processed_measurements]
        return make_response(jsonify(valid_processed_measurements_list), 200)
    else:
        return make_response(jsonify('Daily Valid Measurements not found'), 404)
