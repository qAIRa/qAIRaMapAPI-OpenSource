from flask import jsonify, make_response, redirect, request
from flask_socketio import join_room
import datetime
import dateutil.parser
import dateutil.tz
import os
from passlib.hash import bcrypt

from project import app, db, socketio
from project.database.models import Qhawax, ProcessedMeasurement
import project.main.data.data_helper as helper
import project.main.business.business_helper as business_helper
from sqlalchemy import or_
import csv

@app.route('/api/processed_measurements/', methods=['GET'])
def getProcessedData():
    """
    To get processed data

    :type name: string
    :param name: qHAWAX name

    :type interval_minutes: integer
    :param interval_minutes: period of time in minutes

    """
    qhawax_name = request.args.get('name')
    interval_minutes = int(request.args.get('interval_minutes')) \
        if request.args.get('interval_minutes') is not None else 60
    final_timestamp = datetime.datetime.now(dateutil.tz.tzutc()) - datetime.timedelta(hours=5)
    initial_timestamp = final_timestamp - datetime.timedelta(minutes=interval_minutes) 
    processed_measurements = helper.queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp)

    if processed_measurements is not None:
        processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
        return make_response(jsonify(processed_measurements_list), 200)

    else:
        return make_response(jsonify('Measurements not found'), 404)

@app.route('/api/dataProcessed/', methods=['POST'])
def handleProcessedData():
    """
    To get processed data

    Json data to store processed measurement and valid processed measurement

    """
    try:
        flag_email = False
        data_json = request.get_json()
        product_id = data_json['ID']
        arr_season=[2.62,1.88,1.96,1.15,1.39] #Arreglo de 25C 
        data_json = helper.gasConversionPPBtoMG(data_json, arr_season)
        data_json = helper.roundUpThree(data_json)
        helper.storeProcessedDataInDB(data_json)
        qhawax_id = helper.getQhawaxId(product_id)
        qhawax_zone = "Zona No Definida"
        data_json['ID'] = product_id
        data_json['zone'] = qhawax_zone
        mode = helper.getQhawaxMode(qhawax_id)
        inca_value = helper.getMainIncaQhawaxTable(product_id)
        if(inca_value == -1):
            if(mode=="Cliente"): flag_email = True
            business_helper.saveStatusOn(product_id)
            business_helper.saveTurnOnLastTime(product_id)
            business_helper.updateMainIncaInDB(0,product_id)
            description="Se prendió el qHAWAX"
            observation_type="Interna"
            business_helper.writeBitacora(product_id,observation_type,description,None,None,None)
        if(mode == "Cliente"):
            if(flag_email == True): 
                comercial_name = helper.getComercialName(qhawax_id)
                subject = 'qHAWAX: %s Recuperó Señal' % (comercial_name)
                content1 = 'qHAWAX %s' % (product_id)
                content2 = '\nRecuperó señal: %s' % (data_json['timestamp'])
                response = business_helper.setEmailBody(bcrypt.hash(app.config['SECRET_KEY']), subject, content1, content2)
            qhawax_zone = helper.getNoiseData(product_id)
            data_json['zone'] = qhawax_zone
            minutes_difference,last_time_turn_on = helper.getHoursDifference(qhawax_id)
            if(minutes_difference<5):
                if(last_time_turn_on + datetime.timedelta(minutes=10) < datetime.datetime.now()-datetime.timedelta(hours=5)):
                    helper.storeValidProcessedDataInDB(data_json, qhawax_id, product_id)
                    if(inca_value==0.0):
                        business_helper.updateMainIncaInDB(1,product_id)
            elif(minutes_difference>=5):
                if(last_time_turn_on + datetime.timedelta(hours=2) < datetime.datetime.now()-datetime.timedelta(hours=5)):
                    helper.storeValidProcessedDataInDB(data_json, qhawax_id,product_id)
                    if(inca_value==0.0):
                        business_helper.updateMainIncaInDB(1,product_id)
        socketio.emit('new_data_summary_processed', data_json)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)


@app.route('/api/average_processed_measurements_period/', methods=['GET'])
def getAverageProcessedMeasurementsTimePeriod():
    """
    To get average processed data in a period of time

    :type name: string
    :param name: qHAWAX name

    :type initial_timestamp: timestamp
    :param initial_timestamp: initial time

    :type final_timestamp: timestamp
    :param final_timestamp: last time

    """
    qhawax_name = request.args.get('name')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    processed_measurements = helper.queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp)

    if processed_measurements is not None:
        processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
        averaged_measurements_list = helper.averageMeasurementsInHours(processed_measurements_list, initial_timestamp, final_timestamp, 1)
        return make_response(jsonify(averaged_measurements_list), 200)
    return make_response(jsonify('Measurements not found'), 404)


@app.route('/api/processed_measurements_period/', methods=['GET'])
def getProcessedMeasurementsTimePeriod():
    qhawax_name = request.args.get('name')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    processed_measurements = helper.queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp)

    if processed_measurements is not None:
        processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
        return make_response(jsonify(processed_measurements_list), 200)
    return make_response(jsonify('Measurements not found'), 404)


@app.route('/api/processed_measurements_period_byCompany/', methods=['GET'])
def getProcessedMeasurementsTimePeriodByCompany():
    qhawax_id = request.args.get('qhawax_id')
    company_id = request.args.get('company_id')
    initial_timestamp = dateutil.parser.parse(request.args.get('initial_timestamp'))
    final_timestamp = dateutil.parser.parse(request.args.get('final_timestamp'))
    processed_measurements=[]
    if(int(company_id)!=1):
        if (helper.qhawaxBelongsCompany(qhawax_id,company_id)):   
            processed_measurements = helper.queryDBProcessedByQhawaxByCompany(qhawax_id, initial_timestamp, final_timestamp)
    elif (int(company_id)==1):
        processed_measurements = helper.queryDBProcessedByQhawaxByCompany(qhawax_id, initial_timestamp, final_timestamp)
    if processed_measurements is not None:
        processed_measurements_list = [measurement._asdict() for measurement in processed_measurements]
        return make_response(jsonify(processed_measurements_list), 200)
    return make_response(jsonify('Measurements not found'), 404)


@app.route('/api/importProcessedData/', methods=['POST'])
def importProcessedData():
    try:
        file = request.args.get('csv_file')
        with open(file, 'r') as f:
            reader = csv.reader(f)
            next(reader) # Skip the header row.
            for row in reader:
                data_json = {"ID": row[0], "timestamp": row[1], "temperature": float(row[2]), "pressure": float(row[3]), "humidity": float(row[4]), "spl": float(row[5]),
                        "UV": float(row[6]), "UVA": float(row[7]), "UVB": float(row[8]),"CO": float(row[9]), "H2S": float(row[10]), "NO2": float(row[11]), "O3": float(row[12]), 
                        "SO2": float(row[13]),"PM1": float(row[14]), "PM25": float(row[15]), "PM10": float(row[16]), "lat": float(row[17]), "lon": float(row[18]),"VOC": 0.0 }
                data_json = helper.checkNegatives(data_json)
                product_id = data_json['ID']
                arr_season=[2.62,1.88,1.96,1.15,1.39] #Arreglo de 25C 
                data_json = helper.gasConversionPPBtoMG(data_json, arr_season)
                data_json = helper.roundUpThree(data_json)
                qhawax_id = helper.getQhawaxId(product_id)
                helper.storeProcessedDataInDB(data_json)
                helper.storeValidProcessedDataInDB(data_json, qhawax_id, product_id)
        return make_response('OK', 200)
    except TypeError as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)

