import datetime
import math

import project.main.exceptions as exceptions
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db
from project.database.models import (AirQualityMeasurement, DroneFlightLog,
                                     DroneTelemetry, GasInca,
                                     ProcessedMeasurement, Qhawax,
                                     QhawaxInstallationHistory, TripLog,
                                     ValidProcessedMeasurement)

session = db.session
sensor_array = ["CO", "H2S", "NO2", "O3", "PM25", "PM10", "SO2"]
mobile_sensor_array = [
    "CO",
    "H2S",
    "NO2",
    "O3",
    "PM25",
    "PM10",
    "SO2",
    "CO2",
    "VOC",
]


def queryDBValidAirQuality(
    qhawax_id, initial_timestamp, final_timestamp
):  # validar con sabri
    """Helper function to get Air Quality measurement"""
    sensors = (
        AirQualityMeasurement.CO_ug_m3,
        AirQualityMeasurement.H2S_ug_m3,
        AirQualityMeasurement.NO2_ug_m3,
        AirQualityMeasurement.PM25,
        AirQualityMeasurement.PM10,
        AirQualityMeasurement.SO2_ug_m3,
        AirQualityMeasurement.uv.label("UV"),
        AirQualityMeasurement.spl.label("SPL"),
        AirQualityMeasurement.humidity,
        AirQualityMeasurement.pressure,
        AirQualityMeasurement.O3_ug_m3,
        AirQualityMeasurement.temperature,
        AirQualityMeasurement.lat,
        AirQualityMeasurement.lon,
        AirQualityMeasurement.timestamp_zone,
    )

    if same_helper.qhawaxExistBasedOnID(qhawax_id):
        valid_processed_measurements = (
            session.query(*sensors)
            .filter(AirQualityMeasurement.qhawax_id == qhawax_id)
            .filter(AirQualityMeasurement.timestamp_zone >= initial_timestamp)
            .filter(AirQualityMeasurement.timestamp_zone <= final_timestamp)
            .order_by(AirQualityMeasurement.timestamp_zone)
            .all()
        )
        return [
            measurement._asdict()
            for measurement in valid_processed_measurements
        ]
    return None


def queryDBGasAverageMeasurement(qhawax_name, gas_name):
    """Helper function to get gas average measurement based on qHAWAX name and sensor name"""
    gas_name = exceptions.checkVariable_helper(gas_name, str)

    if gas_name not in sensor_array:
        raise ValueError(
            "Sensor name "
            + str(gas_name)
            + " should be CO, H2S, NO2, O3, PM25, PM10 or SO2"
        )

    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id != None:
        initial_timestamp = datetime.datetime.now()
        last_timestamp = datetime.datetime.now() - datetime.timedelta(hours=24)

        column_array = [
            AirQualityMeasurement.CO.label("sensor"),
            AirQualityMeasurement.H2S.label("sensor"),
            AirQualityMeasurement.NO2.label("sensor"),
            AirQualityMeasurement.O3.label("sensor"),
            AirQualityMeasurement.PM25.label("sensor"),
            AirQualityMeasurement.PM10.label("sensor"),
            AirQualityMeasurement.SO2.label("sensor"),
        ]

        for i in range(len(sensor_array)):
            if gas_name == sensor_array[i]:
                sensors = (
                    AirQualityMeasurement.timestamp_zone,
                    column_array[i],
                )

        return (
            session.query(*sensors)
            .filter(AirQualityMeasurement.qhawax_id == qhawax_id)
            .filter(AirQualityMeasurement.timestamp_zone >= last_timestamp)
            .filter(AirQualityMeasurement.timestamp_zone <= initial_timestamp)
            .order_by(AirQualityMeasurement.timestamp_zone.asc())
            .all()
        )
    return None


def queryDBGasInca(initial_timestamp, final_timestamp):
    """Helper function to get GAS INCA measurement between the specified timestamps"""
    inca_columns = (
        GasInca.CO,
        GasInca.H2S,
        GasInca.SO2,
        GasInca.NO2,
        GasInca.O3,
        GasInca.PM25,
        GasInca.PM10,
        GasInca.SO2,
        GasInca.timestamp_zone,
        GasInca.qhawax_id,
        GasInca.main_inca,
        Qhawax.name.label("qhawax_name"),
    )

    gas_inca = (
        session.query(*inca_columns)
        .join(Qhawax, GasInca.qhawax_id == Qhawax.id)
        .group_by(Qhawax.id, GasInca.id)
        .filter(GasInca.timestamp_zone >= initial_timestamp)
        .filter(GasInca.timestamp_zone <= final_timestamp)
        .all()
    )
    return [measurement._asdict() for measurement in gas_inca]


def queryDBProcessed(qhawax_name, initial_timestamp, final_timestamp):
    """Helper function to get Processed Measurement filter by qHAWAX between the specified timestamps"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        sensors = (
            ProcessedMeasurement.CO,
            ProcessedMeasurement.CO2,
            ProcessedMeasurement.H2S,
            ProcessedMeasurement.NO,
            ProcessedMeasurement.NO2,
            ProcessedMeasurement.O3,
            ProcessedMeasurement.PM1,
            ProcessedMeasurement.PM25,
            ProcessedMeasurement.PM10,
            ProcessedMeasurement.SO2,
            ProcessedMeasurement.VOC,
            ProcessedMeasurement.UV,
            ProcessedMeasurement.UVA,
            ProcessedMeasurement.UVB,
            ProcessedMeasurement.spl,
            ProcessedMeasurement.humidity,
            ProcessedMeasurement.pressure,
            ProcessedMeasurement.temperature,
            ProcessedMeasurement.lat,
            ProcessedMeasurement.lon,
            ProcessedMeasurement.alt,
            ProcessedMeasurement.timestamp_zone,
            ProcessedMeasurement.CO_ug_m3,
            ProcessedMeasurement.H2S_ug_m3,
            ProcessedMeasurement.NO2_ug_m3,
            ProcessedMeasurement.O3_ug_m3,
            ProcessedMeasurement.SO2_ug_m3,
            ProcessedMeasurement.I_temperature,
        )

        processed_measurements = (
            session.query(*sensors)
            .filter(ProcessedMeasurement.qhawax_id == qhawax_id)
            .filter(ProcessedMeasurement.timestamp_zone >= initial_timestamp)
            .filter(ProcessedMeasurement.timestamp_zone <= final_timestamp)
            .order_by(ProcessedMeasurement.timestamp_zone)
            .all()
        )
        all_measurement = []
        for measurement in processed_measurements:
            measurement = measurement._asdict()
            for key, value in measurement.items():
                if (type(value) is float) and math.isnan(value):
                    measurement[key] = None
            all_measurement.append(measurement)
        return all_measurement
    return None


def queryDBValidProcessed(qhawax_name, initial_timestamp, final_timestamp):

    qhawax_installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if qhawax_installation_id is not None:
        sensors = (
            ValidProcessedMeasurement.CO,
            ValidProcessedMeasurement.H2S,
            ValidProcessedMeasurement.NO2,
            ValidProcessedMeasurement.O3,
            ValidProcessedMeasurement.PM25,
            ValidProcessedMeasurement.PM10,
            ValidProcessedMeasurement.SO2,
            ValidProcessedMeasurement.humidity,
            ValidProcessedMeasurement.pressure,
            ValidProcessedMeasurement.temperature,
            ValidProcessedMeasurement.lat,
            ValidProcessedMeasurement.lon,
            ValidProcessedMeasurement.timestamp_zone,
            ValidProcessedMeasurement.CO_ug_m3,
            ValidProcessedMeasurement.H2S_ug_m3,
            ValidProcessedMeasurement.NO2_ug_m3,
            ValidProcessedMeasurement.O3_ug_m3,
            ValidProcessedMeasurement.SO2_ug_m3,
            ValidProcessedMeasurement.I_temperature,
        )

        valid_processed_measurements = (
            session.query(*sensors)
            .filter(
                ValidProcessedMeasurement.qhawax_installation_id
                == qhawax_installation_id
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone >= initial_timestamp
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone <= final_timestamp
            )
            .order_by(ValidProcessedMeasurement.timestamp_zone)
            .all()
        )
        all_measurement = []
        for measurement in valid_processed_measurements:
            measurement = measurement._asdict()
            for key, value in measurement.items():
                if (type(value) is float) and math.isnan(value):
                    measurement[key] = None
            all_measurement.append(measurement)
        return all_measurement
    return None


def queryLastMainInca(qhawax_name):
    """Helper function to get last main inca based on qHAWAX name"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        inca = (
            session.query(GasInca.main_inca)
            .filter(GasInca.qhawax_id == qhawax_id)
            .order_by(GasInca.id)
            .all()
        )
        if inca == []:
            return None
        return (
            session.query(GasInca.main_inca)
            .filter(GasInca.qhawax_id == qhawax_id)
            .order_by(GasInca.id.desc())
            .first()[0]
        )
    return None


def getFirstTimestampValidProcessed(qhawax_id):
    """Helper qHAWAX Installation function to get first timestamp of Valid Processed"""
    installation_id = same_helper.getInstallationId(qhawax_id)
    if installation_id is not None:
        first_timestamp = (
            session.query(ValidProcessedMeasurement.timestamp_zone)
            .filter(
                ValidProcessedMeasurement.qhawax_installation_id
                == int(installation_id)
            )
            .order_by(ValidProcessedMeasurement.timestamp_zone.asc())
            .first()
        )
        return None if (first_timestamp == None) else first_timestamp[0]
    return None


def queryFlightsFilterByTime(initial_timestamp, final_timestamp):
    """Function that returns all the flights between the specified dates"""
    flight_columns = (
        DroneFlightLog.flight_start,
        DroneFlightLog.flight_end,
        QhawaxInstallationHistory.comercial_name,
        DroneFlightLog.flight_detail,
        Qhawax.name.label("qhawax_name"),
        QhawaxInstallationHistory.lat.label("last_latitude_position"),
        QhawaxInstallationHistory.lon.label("last_longitude_position"),
    )

    flight = (
        session.query(*flight_columns)
        .join(Qhawax, DroneFlightLog.qhawax_id == Qhawax.id)
        .join(
            QhawaxInstallationHistory,
            DroneFlightLog.qhawax_id == QhawaxInstallationHistory.qhawax_id,
        )
        .group_by(Qhawax.id, DroneFlightLog.id, QhawaxInstallationHistory.id)
        .filter(initial_timestamp <= DroneFlightLog.flight_start)
        .filter(final_timestamp >= DroneFlightLog.flight_end)
        .order_by(DroneFlightLog.id)
        .all()
    )
    new_flight = []
    for f in flight:
        f = f._asdict()
        f["flight_start"] = util_helper.beautyFormatDate(f["flight_start"])
        f["flight_end"] = util_helper.beautyFormatDate(f["flight_end"])
        new_flight.append(f)
    return new_flight


def queryMobileTripsByTimestamp(initial_timestamp, final_timestamp):
    trip_columns = (
        TripLog.trip_start,
        TripLog.trip_end,
        TripLog.id.label("trip_id"),
        QhawaxInstallationHistory.comercial_name,
        TripLog.details,
        Qhawax.name.label("qhawax_name"),
        QhawaxInstallationHistory.lat.label("last_latitude_position"),
        QhawaxInstallationHistory.lon.label("last_longitude_position"),
    )

    trip = (
        session.query(*trip_columns)
        .join(Qhawax, TripLog.qhawax_id == Qhawax.id)
        .join(
            QhawaxInstallationHistory,
            TripLog.qhawax_id == QhawaxInstallationHistory.qhawax_id,
        )
        .group_by(Qhawax.id, TripLog.id, QhawaxInstallationHistory.id)
        .filter(QhawaxInstallationHistory.end_date_zone == None)
        .filter(initial_timestamp <= TripLog.trip_start)
        .filter(final_timestamp >= TripLog.trip_end)
        .order_by(TripLog.id)
        .all()
    )
    if trip != None:
        new_trip = []
        for t in trip:
            t = t._asdict()
            t["trip_start"] = util_helper.beautyFormatDate(t["trip_start"])
            t["trip_end"] = util_helper.beautyFormatDate(t["trip_end"])
            new_trip.append(t)
        return new_trip
    return None


def queryDBTelemetry(qhawax_name, initial_timestamp, final_timestamp):
    """Helper function to get Telemetry filter by qHAWAX between timestamp"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        sensors = (
            DroneTelemetry.airspeed,
            DroneTelemetry.alt,
            DroneTelemetry.battery_perc,
            DroneTelemetry.dist_home,
            DroneTelemetry.flight_mode,
            DroneTelemetry.lat,
            DroneTelemetry.lon,
            DroneTelemetry.num_gps,
            DroneTelemetry.voltage,
            DroneTelemetry.velocity_variance,
            DroneTelemetry.timestamp,
            DroneTelemetry.current,
            DroneTelemetry.fix_type,
        )

        telemetry = (
            session.query(*sensors)
            .filter(DroneTelemetry.qhawax_id == qhawax_id)
            .filter(DroneTelemetry.timestamp >= initial_timestamp)
            .filter(DroneTelemetry.timestamp <= final_timestamp)
            .order_by(DroneTelemetry.timestamp)
            .all()
        )
        return [t._asdict() for t in telemetry]
    return None


def queryDBProcessedByPollutant(
    qhawax_name, initial_timestamp, final_timestamp, pollutant
):
    """Helper function to get Processed Measurement filter by qHAWAX between timestamp"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        column_array = [
            ProcessedMeasurement.CO.label("pollutant"),
            ProcessedMeasurement.H2S.label("pollutant"),
            ProcessedMeasurement.NO2.label("pollutant"),
            ProcessedMeasurement.O3.label("pollutant"),
            ProcessedMeasurement.PM25.label("pollutant"),
            ProcessedMeasurement.PM10.label("pollutant"),
            ProcessedMeasurement.SO2.label("pollutant"),
            ProcessedMeasurement.CO2.label("pollutant"),
            ProcessedMeasurement.VOC.label("pollutant"),
        ]
        # sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']
        for i in range(len(mobile_sensor_array)):
            if pollutant == mobile_sensor_array[i]:
                sensors = (
                    ProcessedMeasurement.timestamp_zone,
                    column_array[i],
                    ProcessedMeasurement.lat,
                    ProcessedMeasurement.lon,
                )

        measurements = (
            session.query(*sensors)
            .filter(ProcessedMeasurement.qhawax_id == qhawax_id)
            .filter(ProcessedMeasurement.timestamp_zone >= initial_timestamp)
            .filter(ProcessedMeasurement.timestamp_zone <= final_timestamp)
            .order_by(ProcessedMeasurement.timestamp_zone.asc())
            .all()
        )
        return [t._asdict() for t in measurements]
    return None


def queryDBProcessedByPollutantMobile(
    qhawax_name, initial_timestamp, final_timestamp, pollutant
):
    """Helper function to get Processed Measurement filter by qHAWAX between timestamp"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        column_array = [
            ProcessedMeasurement.CO.label("pollutant"),
            ProcessedMeasurement.H2S.label("pollutant"),
            ProcessedMeasurement.NO2.label("pollutant"),
            ProcessedMeasurement.O3.label("pollutant"),
            ProcessedMeasurement.PM25.label("pollutant"),
            ProcessedMeasurement.PM10.label("pollutant"),
            ProcessedMeasurement.SO2.label("pollutant"),
            ProcessedMeasurement.CO2.label("pollutant"),
            ProcessedMeasurement.VOC.label("pollutant"),
        ]
        # sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']
        for i in range(len(mobile_sensor_array)):
            if pollutant == mobile_sensor_array[i]:
                sensors = (
                    ProcessedMeasurement.timestamp_zone,
                    column_array[i],
                    ProcessedMeasurement.lat,
                    ProcessedMeasurement.lon,
                )

        measurements = (
            session.query(*sensors)
            .filter(ProcessedMeasurement.qhawax_id == qhawax_id)
            .filter(ProcessedMeasurement.timestamp_zone >= initial_timestamp)
            .filter(ProcessedMeasurement.timestamp_zone <= final_timestamp)
            .order_by(ProcessedMeasurement.timestamp_zone.asc())
            .all()
        )

        factor_final_json = {
            "CO": 100 / 10000,
            "NO2": 100 / 200,
            "PM10": 100 / 150,
            "PM25": 100 / 25,
            "SO2": 100 / 20,
            "O3": 100 / 120,
            "H2S": 100 / 150,
        }
        values = []
        if pollutant in factor_final_json:
            for t in measurements:
                dictValue = t._asdict()
                dictValue["pollutant"] = round(
                    dictValue["pollutant"] * factor_final_json[pollutant], 3
                )
                values.append(dictValue)
            return values
        else:
            return [t._asdict() for t in measurements]

    return None


def queryDBValidProcessedByPollutantMobile(
    qhawax_name, initial_timestamp, final_timestamp, pollutant
):
    """Helper function to get Valid Processed Measurement filter by qHAWAX between timestamp"""
    qhawax_installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if qhawax_installation_id is not None:
        column_array = [
            ValidProcessedMeasurement.CO.label("pollutant"),
            ValidProcessedMeasurement.H2S.label("pollutant"),
            ValidProcessedMeasurement.NO2.label("pollutant"),
            ValidProcessedMeasurement.O3.label("pollutant"),
            ValidProcessedMeasurement.PM25.label("pollutant"),
            ValidProcessedMeasurement.PM10.label("pollutant"),
            ValidProcessedMeasurement.SO2.label("pollutant"),
            ValidProcessedMeasurement.CO2.label("pollutant"),
            ValidProcessedMeasurement.VOC.label("pollutant"),
        ]
        # sensor_array = ['CO','H2S','NO2','O3','PM25','PM10','SO2']
        for i in range(len(mobile_sensor_array)):
            if pollutant == mobile_sensor_array[i]:
                sensors = (
                    ValidProcessedMeasurement.timestamp_zone,
                    column_array[i],
                    ValidProcessedMeasurement.lat,
                    ValidProcessedMeasurement.lon,
                )

        measurements = (
            session.query(*sensors)
            .filter(
                ValidProcessedMeasurement.qhawax_installation_id
                == qhawax_installation_id
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone >= initial_timestamp
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone <= final_timestamp
            )
            .order_by(ValidProcessedMeasurement.timestamp_zone.asc())
            .all()
        )

        factor_final_json = {
            "CO": 100 / 10000,
            "NO2": 100 / 200,
            "PM10": 100 / 150,
            "PM25": 100 / 25,
            "SO2": 100 / 20,
            "O3": 100 / 120,
            "H2S": 100 / 150,
        }
        values = []
        if pollutant in factor_final_json:
            for t in measurements:
                dictValue = t._asdict()
                dictValue["pollutant"] = round(
                    dictValue["pollutant"] * factor_final_json[pollutant], 3
                )
                values.append(dictValue)
            return values
        else:
            return [t._asdict() for t in measurements]

    return None


def queryDBValidProcessedMeasurementsSimulationMobile(
    qhawax_name, initial_timestamp, final_timestamp
):
    qhawax_installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if qhawax_installation_id is not None:
        sensors = (
            ValidProcessedMeasurement.CO,
            ValidProcessedMeasurement.H2S,
            ValidProcessedMeasurement.NO2,
            ValidProcessedMeasurement.O3,
            ValidProcessedMeasurement.PM25,
            ValidProcessedMeasurement.PM10,
            ValidProcessedMeasurement.SO2,
            ValidProcessedMeasurement.timestamp_zone,
            ValidProcessedMeasurement.lat,
            ValidProcessedMeasurement.lon,
        )
        validMeasurements = (
            session.query(*sensors)
            .filter(
                ValidProcessedMeasurement.qhawax_installation_id
                == qhawax_installation_id
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone >= initial_timestamp
            )
            .filter(
                ValidProcessedMeasurement.timestamp_zone <= final_timestamp
            )
            .order_by(ValidProcessedMeasurement.timestamp_zone.asc())
            .all()
        )

        factor_final_json = {
            "CO": 100 / 10000,
            "NO2": 100 / 200,
            "PM10": 100 / 150,
            "PM25": 100 / 25,
            "SO2": 100 / 20,
            "O3": 100 / 100,
            "H2S": 100 / 150,
        }
        values = []
        for t in validMeasurements:
            dictValue = t._asdict()
            for key in factor_final_json:
                if dictValue[key] != None:
                    dictValue[key] = round(
                        dictValue[key] * factor_final_json[key], 3
                    )
            # print(dictValue) # json
            # {'CO': 2076.038, 'H2S': 17.78, 'NO2': 75.955, 'O3': -16.706, 'PM25': 42.196, 'PM10': 69.863, 'SO2': 47.115, 'CO2': None, 'VOC': None, 'timestamp_zone': datetime.datetime(2021, 6, 14, 14, 59, 57, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0,
            # name=None)), 'lat': -12.048906, 'lon': -77.037643}
            values.append(dictValue)

        return values


def qHAWAXIsInFlight(qhawax_name):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        flight = (
            session.query(DroneFlightLog.flight_start)
            .filter(
                DroneFlightLog.qhawax_id == qhawax_id,
                DroneFlightLog.flight_end == None,
            )
            .order_by(DroneFlightLog.id)
            .all()
        )
        if flight != []:
            return flight[0][0]
    return None


def qHAWAXIsInTrip(qhawax_name):
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        trip = (
            session.query(TripLog.trip_start)
            .filter(TripLog.qhawax_id == qhawax_id, TripLog.trip_end == None)
            .order_by(TripLog.id)
            .all()
        )
        if trip != []:
            return trip[0][0]
    return None


def AllqHAWAXIsInFlight():
    flight = (
        session.query(
            DroneFlightLog.flight_start,
            Qhawax.name,
            QhawaxInstallationHistory.comercial_name,
        )
        .join(Qhawax, DroneFlightLog.qhawax_id == Qhawax.id)
        .join(
            QhawaxInstallationHistory,
            Qhawax.id == QhawaxInstallationHistory.qhawax_id,
        )
        .group_by(Qhawax.id, DroneFlightLog.id, QhawaxInstallationHistory.id)
        .filter(DroneFlightLog.flight_end == None)
        .order_by(DroneFlightLog.id)
        .all()
    )
    return [t._asdict() for t in flight]


def AllqHAWAXIsInTrip():
    trip = (
        session.query(
            TripLog.trip_start,
            Qhawax.name,
            QhawaxInstallationHistory.comercial_name,
        )
        .join(Qhawax, TripLog.qhawax_id == Qhawax.id)
        .join(
            QhawaxInstallationHistory,
            Qhawax.id == QhawaxInstallationHistory.qhawax_id,
        )
        .group_by(Qhawax.id, TripLog.id, QhawaxInstallationHistory.id)
        .filter(
            TripLog.trip_end == None,
            QhawaxInstallationHistory.end_date_zone == None,
        )
        .order_by(TripLog.id)
        .all()
    )
    return [t._asdict() for t in trip]


def getQhawaxLatestTimestampProcessedMeasurement(qhawax_name):
    """Helper qHAWAX function to get latest timestamp in UTC 00 from Processed Measurement"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        qhawax_time = (
            session.query(ProcessedMeasurement.timestamp_zone)
            .filter_by(qhawax_id=qhawax_id)
            .first()
        )
        processed_measurement_timestamp = ""
        if qhawax_time != None:
            processed_measurement_timestamp = (
                session.query(ProcessedMeasurement.timestamp_zone)
                .filter_by(qhawax_id=qhawax_id)
                .order_by(ProcessedMeasurement.id.desc())
                .first()
                .timestamp_zone
            )
            return processed_measurement_timestamp
    return None


def getQhawaxLatestTimestampValidProcessedMeasurement(qhawax_name):
    """Helper qHAWAX function to get latest timestamp in UTC 00 from Processed Measurement"""
    qhawax_installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if qhawax_installation_id is not None:
        qhawax_time = (
            session.query(ValidProcessedMeasurement.timestamp_zone)
            .filter_by(qhawax_installation_id=qhawax_installation_id)
            .first()
        )
        valid_measurement_timestamp = ""
        if qhawax_time != None:
            valid_measurement_timestamp = (
                session.query(ValidProcessedMeasurement.timestamp_zone)
                .filter_by(qhawax_installation_id=qhawax_installation_id)
                .order_by(ValidProcessedMeasurement.timestamp_zone.desc())
                .first()
                .timestamp_zone
            )
            return valid_measurement_timestamp
    return None


def getMobileLatestLatLonValidProcessedMeasurement(qhawax_name):
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if installation_id is not None:
        values = (
            session.query(
                ValidProcessedMeasurement.lat, ValidProcessedMeasurement.lon
            )
            .filter_by(qhawax_installation_id=installation_id)
            .order_by(ValidProcessedMeasurement.id.desc())
            .first()
        )
        return values._asdict()
    return None


def getqHAWAXMobileTripByTurn(qhawax_name, turn, id):
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if installation_id != None:
        query = session.query(TripLog.trip_start).filter_by(id=id).first()
        if query != None:
            trip_time = query[0]
            (
                start_time,
                finish_time,
            ) = util_helper.getStartAndFinishTimestampBasedOnTurnAndTimestampMobile(
                trip_time, turn
            )
            return queryDBValidProcessedMeasurementsSimulationMobile(
                qhawax_name, start_time, finish_time
            )
    return None


def getqHAWAXMobileLatestTripStart(qhawax_name):
    # Returns the latest trip_start of the target qHAWAX - datetime.datetime format
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id != None:
        query = (
            session.query(TripLog.trip_start, TripLog.id)
            .join(
                QhawaxInstallationHistory,
                QhawaxInstallationHistory.qhawax_id == TripLog.qhawax_id,
            )
            .filter(
                QhawaxInstallationHistory.end_date_zone == None,
                TripLog.qhawax_id == qhawax_id,
            )
            .order_by(TripLog.trip_start.desc())
            .first()
        )
        if query != None:
            # 2021-07-09 12:29:44
            queryTimestamp = query[0].replace(microsecond=0, tzinfo=None)
            return queryTimestamp, query[1]
    return None, None
