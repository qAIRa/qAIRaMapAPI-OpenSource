import datetime
import time
from datetime import timedelta

import dateutil.parser
import dateutil.tz

import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
import project.main.exceptions as exceptions
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db, socketio
from project.database.models import (AirQualityMeasurement, DroneFlightLog,
                                     DroneTelemetry, GasInca,
                                     ProcessedMeasurement, Qhawax,
                                     QhawaxInstallationHistory, TripLog,
                                     ValidProcessedMeasurement)

session = db.session
MAX_SECONDS_DATA_STORAGE = 20
drone_elapsed_time = None
drone_telemetry = None
drone_storage = {}
pollutants = ["CO", "CO2", "NO2", "O3", "H2S", "SO2", "PM25", "PM10", "VOC"]


def storeAirQualityDataInDB(data):
    """Helper function to record Air Quality measurement"""
    data = exceptions.checkVariable_helper(data, dict)
    qhawax_name = data.pop("ID", None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id != None:
        air_quality_data = {
            "CO": data["CO"],
            "CO_ug_m3": data["CO_ug_m3"],
            "H2S": data["H2S"],
            "H2S_ug_m3": data["H2S_ug_m3"],
            "SO2": data["SO2"],
            "SO2_ug_m3": data["SO2_ug_m3"],
            "NO2": data["NO2"],
            "NO2_ug_m3": data["NO2_ug_m3"],
            "O3_ug_m3": data["O3_ug_m3"],
            "PM25": data["PM25"],
            "PM10": data["PM10"],
            "O3": data["O3"],
            "lat": data["lat"],
            "lon": data["lon"],
            "alt": data["alt"],
            "uv": data["UV"],
            "spl": data["SPL"],
            "temperature": data["temperature"],
            "timestamp_zone": data["timestamp_zone"],
            "I_temperature": data["I_temperature"],
            "humidity": data["humidity"],
            "pressure": data["pressure"],
        }
        air_quality_measurement = AirQualityMeasurement(
            **air_quality_data, qhawax_id=qhawax_id
        )
        session.add(air_quality_measurement)
        session.commit()


def storeGasIncaInDB(data):
    """Helper function to record GAS INCA measurement"""
    data = exceptions.checkVariable_helper(data, dict)
    gas_inca_data = {
        "CO": data["CO"],
        "H2S": data["H2S"],
        "SO2": data["SO2"],
        "NO2": data["NO2"],
        "timestamp_zone": data["timestamp_zone"],
        "O3": data["O3"],
        "PM25": data["PM25"],
        "PM10": data["PM10"],
        "main_inca": data["main_inca"],
    }
    qhawax_name = data.pop("ID", None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_processed = GasInca(**gas_inca_data, qhawax_id=qhawax_id)
    session.add(gas_inca_processed)
    session.commit()


def storeProcessedDataInDB(data):
    """Helper Processed Measurement function to store Processed Data"""
    data = exceptions.checkVariable_helper(data, dict)
    qhawax_name = data.pop("ID", None)
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    processed_measurement = ProcessedMeasurement(**data, qhawax_id=qhawax_id)
    session.add(processed_measurement)
    session.commit()


def storeValidProcessedDataMobileInDB(data, qhawax_id, product_id):
    """Helper Processed Measurement function to insert Valid Processed Data"""
    installation_id = same_helper.getInstallationId(qhawax_id)
    if installation_id != None:
        valid_data = {
            "timestamp": data["timestamp"],
            "CO": data["CO"],
            "CO_ug_m3": data["CO_ug_m3"],
            "H2S": data["H2S"],
            "H2S_ug_m3": data["H2S_ug_m3"],
            "SO2": data["SO2"],
            "SO2_ug_m3": data["SO2_ug_m3"],
            "NO2": data["NO2"],
            "NO2_ug_m3": data["NO2_ug_m3"],
            "O3": data["O3"],
            "O3_ug_m3": data["O3_ug_m3"],
            "PM25": data["PM25"],
            "lat": data["lat"],
            "lon": data["lon"],
            "PM1": data["PM1"],
            "PM10": data["PM10"],
            "UV": data["UV"],
            "UVA": data["UVA"],
            "UVB": data["UVB"],
            "SPL": data["spl"],
            "humidity": data["humidity"],
            "pressure": data["pressure"],
            "temperature": data["temperature"],
            "timestamp_zone": data["timestamp_zone"],
            "I_temperature": data["I_temperature"],
            "VOC": data["VOC"],
            "CO2": data["CO2"],
        }
        valid_processed_measurement = ValidProcessedMeasurement(
            **valid_data, qhawax_installation_id=installation_id
        )
        session.add(valid_processed_measurement)
        session.commit()


def storeValidProcessedDataInDB(data, product_id):
    """Helper Processed Measurement function to insert Valid Processed Data"""
    installation_id = same_helper.getInstallationIdBaseName(product_id)
    if installation_id != None:
        valid_data = {
            "timestamp": data["timestamp"],
            "CO": data["CO"],
            "CO_ug_m3": data["CO_ug_m3"],
            "H2S": data["H2S"],
            "H2S_ug_m3": data["H2S_ug_m3"],
            "SO2": data["SO2"],
            "SO2_ug_m3": data["SO2_ug_m3"],
            "NO2": data["NO2"],
            "NO2_ug_m3": data["NO2_ug_m3"],
            "O3": data["O3"],
            "O3_ug_m3": data["O3_ug_m3"],
            "PM25": data["PM25"],
            "lat": data["lat"],
            "lon": data["lon"],
            "PM1": data["PM1"],
            "PM10": data["PM10"],
            "UV": data["UV"],
            "UVA": data["UVA"],
            "UVB": data["UVB"],
            "SPL": data["spl"],
            "humidity": data["humidity"],
            "CO2": data["CO2"],
            "pressure": data["pressure"],
            "temperature": data["temperature"],
            "timestamp_zone": data["timestamp_zone"],
            "I_temperature": data["I_temperature"],
            "VOC": data["VOC"],
        }
        valid_processed_measurement = ValidProcessedMeasurement(
            **valid_data, qhawax_installation_id=installation_id
        )
        session.add(valid_processed_measurement)
        session.commit()
        data = util_helper.setNoneStringElements(data)
        socketio.emit(data["ID"], data)


def storeValidProcessedDataInDBMobile(data, product_id):
    """Helper Processed Measurement function to insert Valid Processed Data"""
    installation_id = same_helper.getInstallationIdBaseName(product_id)
    if installation_id != None:
        valid_data = {
            "timestamp": data["timestamp"],
            "CO": data["CO"],
            "CO_ug_m3": data["CO_ug_m3"],
            "H2S": data["H2S"],
            "H2S_ug_m3": data["H2S_ug_m3"],
            "SO2": data["SO2"],
            "SO2_ug_m3": data["SO2_ug_m3"],
            "NO2": data["NO2"],
            "NO2_ug_m3": data["NO2_ug_m3"],
            "O3": data["O3"],
            "O3_ug_m3": data["O3_ug_m3"],
            "PM25": data["PM25"],
            "lat": data["lat"],
            "lon": data["lon"],
            "PM1": data["PM1"],
            "PM10": data["PM10"],
            "UV": data["UV"],
            "UVA": data["UVA"],
            "UVB": data["UVB"],
            "SPL": data["spl"],
            "humidity": data["humidity"],
            "CO2": data["CO2"],
            "pressure": data["pressure"],
            "temperature": data["temperature"],
            "timestamp_zone": data["timestamp_zone"],
            "I_temperature": data["I_temperature"],
            "VOC": data["VOC"],
        }
        valid_processed_measurement = ValidProcessedMeasurement(
            **valid_data, qhawax_installation_id=installation_id
        )
        session.add(valid_processed_measurement)
        session.commit()
        data = util_helper.setNoneStringElements(data)
        socketio.emit(data["ID"] + "_mobile", data)


def validAndBeautyJsonValidProcessedMobile(data_json, product_id):
    data_json = exceptions.checkVariable_helper(data_json, dict)
    product_id = exceptions.checkVariable_helper(product_id, str)
    if util_helper.checkValidLatLonValues(data_json):
        if not (
            same_helper.isMobileQhawaxInATrip(product_id)
        ):  # in case trip has finished, a new one has to begin...
            recordStartTrip(product_id)
        storeValidProcessedDataInDBMobile(data_json, product_id)
        max_value = 0
        for i in range(len(pollutants)):
            socket_name = data_json["ID"] + "_" + str(pollutants[i]) + "_valid"
            pollutantStr = (
                str(pollutants[i]) + "_ug_m3"
                if (pollutants[i] in ["CO", "NO2", "O3", "H2S", "SO2"])
                else str(pollutants[i])
            )
            new_data_json = {
                "sensor": pollutants[i],
                "center": {"lat": data_json["lat"], "lng": data_json["lon"]},
            }
            factor_final_json = {
                "CO": 100 / 10000,
                "NO2": 100 / 200,
                "PM10": 100 / 150,
                "PM25": 100 / 25,
                "SO2": 100 / 20,
                "O3": 100 / 100,
                "H2S": 100 / 150,
            }
            if data_json[pollutantStr] != None:
                if pollutants[i] in factor_final_json:
                    data_json[pollutantStr] = round(
                        data_json[pollutantStr]
                        * factor_final_json[pollutants[i]],
                        3,
                    )
                new_data_json[pollutants[i]] = data_json[pollutantStr]
                socketio.emit(socket_name, new_data_json)  # qH006_CO_valid
                if (
                    data_json[pollutantStr] >= max_value
                ):  # same percentage comparison logic to obtain the highest percentage out of all pollutants
                    max_value = data_json[pollutantStr]
                    sensor_name = pollutants[i]
        calInca = util_helper.validaPollutant(max_value, sensor_name)
        post_business_helper.updateMainIncaQhawaxTable(calInca, product_id)
        post_business_helper.updateMainIncaQhawaxInstallationTable(
            calInca, product_id
        )

        # if(inca_value==0.0):
        #   post_business_helper.updateMainIncaInDB(1,product_id)
        #   post_business_helper.updateMainIncaQhawaxInstallationTable(1,product_id)


def validAndBeautyJsonValidProcessed(data_json, product_id, inca_value):
    """Helper function to valid json Valid Processed table"""
    data_json = exceptions.checkVariable_helper(data_json, dict)
    product_id = exceptions.checkVariable_helper(product_id, str)
    storeValidProcessedDataInDB(data_json, product_id)
    if inca_value == 0.0:
        post_business_helper.updateMainIncaQhawaxTable(1, product_id)
        post_business_helper.updateMainIncaQhawaxInstallationTable(
            1, product_id
        )


def validTimeOfValidProcessed(
    time_valid, time_type, last_time_turn_on, data_json, product_id, inca_value
):
    """Helper function to valid time of Valid Processed table"""
    time_valid = exceptions.checkVariable_helper(time_valid, int)
    time_type = exceptions.checkVariable_helper(time_type, str)
    data_json = exceptions.checkVariable_helper(data_json, dict)
    product_id = exceptions.checkVariable_helper(product_id, str)
    aditional_time = (
        datetime.timedelta(hours=time_valid)
        if (time_type == "hour")
        else datetime.timedelta(minutes=time_valid)
    )
    if last_time_turn_on + aditional_time < datetime.datetime.now(
        dateutil.tz.tzutc()
    ):
        validAndBeautyJsonValidProcessed(data_json, product_id, inca_value)


def storeLogs(telemetry, drone_name):
    global drone_elapsed_time, drone_telemetry, drone_storage
    telemetry = exceptions.checkVariable_helper(telemetry, dict)
    drone_name = exceptions.checkVariable_helper(drone_name, str)
    if drone_elapsed_time is None:
        drone_elapsed_time = time.time()

    if drone_name not in drone_storage:
        qhawax_id = (
            same_helper.getQhawaxID(drone_name)
            if same_helper.getQhawaxID(drone_name) is not None
            else "qH001"
        )
        drone_storage[drone_name] = qhawax_id

    if time.time() - drone_elapsed_time > MAX_SECONDS_DATA_STORAGE:
        drone_telemetry = formatTelemetryForStorage(telemetry)
        drone_telemetry["timestamp"] = datetime.datetime.now(
            dateutil.tz.tzutc()
        )
        drone_telemetry["qhawax_id"] = drone_storage[drone_name]
        drone_telemetry = DroneTelemetry(**drone_telemetry)
        session.add(drone_telemetry)
        session.commit()
        drone_elapsed_time = time.time()


def formatTelemetryForStorage(telemetry):
    telemetry = exceptions.checkVariable_helper(telemetry, dict)
    rcout = (
        telemetry["rcout"]
        if telemetry["rcout"] is not None
        else [-1, -1, -1, -1, -1, -1, -1, -1]
    )
    compass1 = (
        telemetry["compass1"]
        if telemetry["compass1"] is not None
        else [-1, -1, -1]
    )
    compass2 = (
        telemetry["compass2"]
        if telemetry["compass2"] is not None
        else [-1, -1, -1]
    )
    gps = (
        telemetry["gps"]
        if telemetry["gps"] is not None
        else {"satellites": -1, "fix_type": -1}
    )
    vibrations = (
        telemetry["vibrations"]
        if telemetry["vibrations"] is not None
        else [-1, -1, -1]
    )

    return {
        "airspeed": telemetry["airspeed"],  # obligatorio
        "alt": telemetry["alt"],  # obligatorio
        "battery_perc": telemetry["level"],  # obligatorio
        "dist_home": telemetry["dist_home"],  # obligatorio
        "compass1_x": compass1[0],  # obligatorio
        "compass1_y": compass1[1],  # obligatorio
        "compass1_z": compass1[2],  # obligatorio
        "compass2_x": compass2[0],  # obligatorio
        "compass2_y": compass2[1],  # obligatorio
        "compass2_z": compass2[2],  # obligatorio
        "compass_variance": telemetry["ekf_status"]["compass_variance"]
        if telemetry["ekf_status"] is not None
        else -1,  # obligatorio
        "current": telemetry["current"],  # obligatorio
        "fix_type": telemetry["fix_type"],  # obligatorio
        "flight_mode": telemetry["flight_mode"],  # obligatorio
        "gps_sats": gps["satellites"],  # obligatorio
        "gps_fix": gps["fix_type"],  # obligatorio
        "gps2_sats": telemetry["gps2"]["satellites"]
        if telemetry["gps2"] is not None
        else -1,  # obligatorio
        "gps2_fix": telemetry["gps2"]["fix_type"]
        if telemetry["gps2"] is not None
        else -1,  # obligatorio
        "irlock_x": telemetry["irlock"][0]
        if telemetry["irlock"] is not None
        else -1,  # obligatorio
        "irlock_y": telemetry["irlock"][1]
        if telemetry["irlock"] is not None
        else -1,  # obligatorio
        "irlock_status": telemetry["IRLOCK_status"],  # obligatorio
        "lat": telemetry["lat"],  # obligatorio
        "lon": telemetry["lon"],  # obligatorio
        "num_gps": telemetry["num_gps"],  # obligatorio
        "pos_horiz_variance": telemetry["ekf_status"]["pos_horiz_variance"]
        if telemetry["ekf_status"] is not None
        else -1,  # obligatorio
        "pos_vert_variance": telemetry["ekf_status"]["pos_vert_variance"]
        if telemetry["ekf_status"] is not None
        else -1,  # obligatorio
        "rcout1": rcout[0],  # obligatorio
        "rcout2": rcout[1],  # obligatorio
        "rcout3": rcout[2],  # obligatorio
        "rcout4": rcout[3],  # obligatorio
        "rcout5": rcout[4],  # obligatorio
        "rcout6": rcout[5],  # obligatorio
        "rcout7": rcout[6],  # obligatorio
        "rcout8": rcout[7],  # obligatorio
        "sonar_dist": telemetry["sonar_dist"],  # obligatorio
        "throttle": telemetry["throttle"],  # obligatorio
        "vibrations_x": vibrations[0],  # obligatorio
        "vibrations_y": vibrations[1],  # obligatorio
        "vibrations_z": vibrations[2],  # obligatorio
        "voltage": telemetry["voltage"],  # obligatorio
        "velocity_variance": telemetry["ekf_status"]["velocity_variance"]
        if telemetry["ekf_status"] is not None
        else -1,  # obligatorio
        "terrain_alt_variance": telemetry["ekf_status"]["terrain_alt_variance"]
        if telemetry["ekf_status"] is not None
        else -1,  # obligatorio
        "waypoint": telemetry["waypoint"],  # obligatorio
        "yaw": telemetry["yaw"],  # obligatorio
    }


def recordDroneTakeoff(flight_start, qhawax_name):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    gas_inca_processed = DroneFlightLog(
        flight_start=flight_start, qhawax_id=qhawax_id
    )
    session.add(gas_inca_processed)
    session.commit()


def recordDroneLanding(flight_end, qhawax_name, flight_detail):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    landing_json = {"flight_end": flight_end, "flight_detail": flight_detail}
    session.query(DroneFlightLog).filter_by(
        qhawax_id=qhawax_id, flight_end=None
    ).update(values=landing_json)
    session.commit()


def deleteValuesBetweenTimestampsProcessedMeasurement(timestamp_before):
    """Helper qHAWAX Installation function that gets values of Processed between timestamps of STATIC qHAWAX"""
    qhawax_static_id_list = get_business_helper.getAllStaticQhawaxID()
    # qhawax_id_list = get_business_helper.queryAllQhawaxID()
    # print("List of all static qhawax")
    # print(qhawax_static_id_list)
    # x = 1
    for qhawax_id in qhawax_static_id_list:
        # if(qhawax_static_id_list[x]==qhawax_id):
        #     print("Entre al id del qhawax " + str(qhawax_id["id"]))
        if qhawax_id["id"] is not None:
            processed_measurement_ids = (
                session.query(
                    ProcessedMeasurement.id, ProcessedMeasurement.qhawax_id
                )
                .join(Qhawax, ProcessedMeasurement.qhawax_id == Qhawax.id)
                .filter(ProcessedMeasurement.timestamp_zone < timestamp_before)
                .filter(ProcessedMeasurement.qhawax_id == qhawax_id["id"])
                .all()
            )
            # return processed_measurement_ids
            # print(len(processed_measurement_ids))
            if processed_measurement_ids != []:
                for each in processed_measurement_ids:
                    deleteThis = (
                        session.query(ProcessedMeasurement)
                        .filter(ProcessedMeasurement.id == int(each[0]))
                        .first()
                    )
                    session.delete(deleteThis)
                    session.commit()
    return "OK"


def deleteValuesBetweenTimestampsValidProcessedMeasurement(timestamp_before):
    """Helper qHAWAX Installation function that gets values of Processed between timestamps of STATIC qHAWAX"""
    qhawax_static_install_id_list = (
        get_business_helper.getAllStaticQhawaxInstallationID()
    )
    # print(qhawax_static_install_id_list)
    # x = len(qhawax_static_install_id_list) - 5
    for qhawax_install_id in qhawax_static_install_id_list:
        # if(qhawax_static_install_id_list[x]==qhawax_install_id):
        #     print("Entre al id del qhawax" + str(qhawax_install_id["id"]))
        if qhawax_install_id["id"] is not None:
            valid_processed_measurement_ids = (
                session.query(
                    ValidProcessedMeasurement.id,
                    ValidProcessedMeasurement.qhawax_installation_id,
                )
                .join(
                    QhawaxInstallationHistory,
                    ValidProcessedMeasurement.qhawax_installation_id
                    == QhawaxInstallationHistory.id,
                )
                .filter(
                    ValidProcessedMeasurement.timestamp_zone < timestamp_before
                )
                .filter(
                    ValidProcessedMeasurement.qhawax_installation_id
                    == qhawax_install_id["id"]
                )
                .all()
            )
            if valid_processed_measurement_ids != []:
                for each in valid_processed_measurement_ids:
                    deleteThis = (
                        session.query(ValidProcessedMeasurement)
                        .filter(ValidProcessedMeasurement.id == int(each[0]))
                        .first()
                    )
                    session.delete(deleteThis)
                    session.commit()
    return "OK"


def recordStartTrip(qhawax_name):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    name = qhawax_name.strip()
    if qhawax_id != None:
        start_trip = datetime.datetime.now(dateutil.tz.tzutc())
        start = TripLog(
            trip_start=datetime.datetime.now(dateutil.tz.tzutc()),
            qhawax_id=qhawax_id,
        )
        session.add(start)
        session.commit()
        socketio.emit(name + "_startTrip", str(start_trip))
        # print("Start trip: ", str(start_trip), "qHAWAX name: ", name + '_startTrip')


def recordEndTrip(qhawax_name, details):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    name = qhawax_name.strip()
    if qhawax_id != None:
        finish_date = (
            session.query(TripLog.trip_end)
            .filter(TripLog.qhawax_id == qhawax_id)
            .order_by(TripLog.id.desc())
            .first()
        )
        if finish_date[0] == None:
            installation_id = same_helper.getInstallationIdBaseName(
                qhawax_name
            )
            if installation_id is not None:
                value = (
                    session.query(ValidProcessedMeasurement.timestamp_zone)
                    .filter_by(qhawax_installation_id=installation_id)
                    .order_by(ValidProcessedMeasurement.id.desc())
                    .first()
                    .timestamp_zone
                )
                socketio.emit(name + "_finishTrip", str(value))
                finish_json = {"trip_end": value, "details": details}
                session.query(TripLog).filter_by(
                    qhawax_id=qhawax_id, trip_end=None
                ).update(values=finish_json)
                session.commit()


def updateLastestLatLonMobile(qhawax_name, json_val):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    session.query(QhawaxInstallationHistory).filter_by(
        qhawax_id=qhawax_id, end_date_zone=None
    ).update(values=json_val)
    # json_val should have {"lat": 12.123, "lon": 12.123}
    session.commit()
