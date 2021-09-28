import datetime
import unittest
from datetime import timedelta

import dateutil
import dateutil.parser
import pytz

import project.main.data.post_data_helper as post_data_helper


class TestPostDataHelper(unittest.TestCase):
    """Test of Post Data Functions"""

    def test_store_air_quality_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.storeAirQualityDataInDB)
        self.assertRaises(
            TypeError, post_data_helper.storeAirQualityDataInDB, True
        )
        self.assertRaises(
            TypeError, post_data_helper.storeAirQualityDataInDB, -5.0
        )
        self.assertRaises(
            TypeError, post_data_helper.storeAirQualityDataInDB, None
        )
        self.assertRaises(
            TypeError, post_data_helper.storeAirQualityDataInDB, "String_"
        )

    def test_store_air_quality_valid(self):
        air_quality_json = {
            "CO": 1986.208,
            "CO_ug_m3": 1986.208,
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "timestamp_zone": "Mon, 04 Jan 2021 01:00:00 GMT",
            "ID": "qH057",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "SPL": 1,
            "UV": 1,
        }
        post_data_helper.storeAirQualityDataInDB(air_quality_json)

    def test_store_gas_inca_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.storeGasIncaInDB)
        self.assertRaises(TypeError, post_data_helper.storeGasIncaInDB, True)
        self.assertRaises(TypeError, post_data_helper.storeGasIncaInDB, -5.0)
        self.assertRaises(TypeError, post_data_helper.storeGasIncaInDB, None)
        self.assertRaises(
            TypeError, post_data_helper.storeGasIncaInDB, "String_"
        )

    def test_store_gas_inca_valid(self):
        gas_inca_json = {
            "CO": 1986.208,
            "H2S": 43.404,
            "NO2": 19.78,
            "O3": 3.126,
            "SO2": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "lat": -12.040278002,
            "lon": -77.0436003,
            "timestamp_zone": "Fri, 01 Jan 2021 00:00:00 GMT",
            "ID": "qH057",
            "main_inca": 1,
        }
        post_data_helper.storeGasIncaInDB(gas_inca_json)

    def test_store_processed_data_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.storeProcessedDataInDB)
        self.assertRaises(
            TypeError, post_data_helper.storeProcessedDataInDB, True
        )
        self.assertRaises(
            TypeError, post_data_helper.storeProcessedDataInDB, -5.0
        )
        self.assertRaises(
            TypeError, post_data_helper.storeProcessedDataInDB, None
        )
        self.assertRaises(
            TypeError, post_data_helper.storeProcessedDataInDB, "String_"
        )

    def test_store_processed_data_valid(self):
        processed_measurement_json = {
            "CO": 1986.208,
            "CO_ug_m3": 1986.208,
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "VOC": 0,
            "CO2": 1,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "UVA": 1,
            "UVB": 1,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "PM1": 1,
            "timestamp_zone": "Mon, 04 Jan 2021 00:00:00 GMT",
            "ID": "qH057",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "spl": 1,
            "UV": 1,
        }
        post_data_helper.storeProcessedDataInDB(processed_measurement_json)
        processed_measurement_json_nan = {
            "CO": "nan",
            "CO_ug_m3": "nan",
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "VOC": 0,
            "CO2": 1,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "UVA": 1,
            "UVB": 1,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "PM1": 1,
            "timestamp_zone": "Mon, 04 Jan 2021 00:00:00 GMT",
            "ID": "qH057",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "spl": 1,
            "UV": 1,
        }
        post_data_helper.storeProcessedDataInDB(processed_measurement_json_nan)

    def test_store_valid_processed_data_not_valid(self):
        self.assertRaises(
            TypeError, post_data_helper.storeValidProcessedDataInDB
        )
        self.assertRaises(
            TypeError, post_data_helper.storeValidProcessedDataInDB, True
        )
        self.assertRaises(
            TypeError, post_data_helper.storeValidProcessedDataInDB, -5.0
        )
        self.assertRaises(
            TypeError, post_data_helper.storeValidProcessedDataInDB, None
        )
        self.assertRaises(
            TypeError, post_data_helper.storeValidProcessedDataInDB, "String_"
        )

    def test_store_valid_processed_data_valid(self):
        processed_measurement_json = {
            "CO": 1986.208,
            "CO_ug_m3": 1986.208,
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "VOC": 0,
            "CO2": 1,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "UVA": 1,
            "UVB": 1,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "PM1": 1,
            "timestamp_zone": "Tue, 05 Jan 2021 05:00:00 GMT",
            "ID": "qH004",
            "timestamp": "Fri, 01 Jan 2021 00:00:00 GMT",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "spl": 1,
            "UV": 1,
        }
        post_data_helper.storeValidProcessedDataInDB(
            processed_measurement_json, "qH004"
        )

    def test_valid_time_of_valid_processed_not_valid(self):
        self.assertRaises(
            TypeError, post_data_helper.validTimeOfValidProcessed
        )
        self.assertRaises(
            TypeError, post_data_helper.validTimeOfValidProcessed, 1
        )
        self.assertRaises(
            TypeError, post_data_helper.validTimeOfValidProcessed, 1, 1
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validTimeOfValidProcessed,
            "a",
            "minute",
            "hora",
            "json",
            23,
            "inca",
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validTimeOfValidProcessed,
            1,
            "minute",
            "hora",
            "json",
            23,
            "inca",
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validTimeOfValidProcessed,
            1,
            "minute",
            "hora",
            {},
            23,
            0.0,
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validTimeOfValidProcessed,
            1,
            "minute",
            "hora",
            {},
            "qH001",
            "inca",
        )

    def test_valid_time_of_valid_processed_valid(self):
        naive_time = datetime.time(0, 0, 0, 410000)
        date = datetime.date(2021, 1, 1)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        last_time_turn_on = timezone.localize(naive_datetime)
        data_json = {
            "CO": 1986.208,
            "CO_ug_m3": 1986.208,
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "VOC": 0,
            "CO2": 1,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "UVA": 1,
            "UVB": 1,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "PM1": 1,
            "ID": "qH057",
            "timestamp_zone": "Fri, 01 Jan 2021 05:00:00 GMT",
            "timestamp": "Fri, 01 Jan 2021 00:00:00 GMT",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "spl": 1,
            "UV": 1,
        }
        inca_value = 0.0
        product_id = "qH057"
        post_data_helper.validTimeOfValidProcessed(
            10, "minute", last_time_turn_on, data_json, product_id, inca_value
        )
        post_data_helper.validTimeOfValidProcessed(
            10, "hour", last_time_turn_on, data_json, product_id, inca_value
        )

    def test_store_valid_and_beauty_json_not_valid(self):
        self.assertRaises(
            TypeError, post_data_helper.validAndBeautyJsonValidProcessed
        )
        self.assertRaises(
            TypeError, post_data_helper.validAndBeautyJsonValidProcessed, True
        )
        self.assertRaises(
            TypeError, post_data_helper.validAndBeautyJsonValidProcessed, -5.0
        )
        self.assertRaises(
            TypeError, post_data_helper.validAndBeautyJsonValidProcessed, None
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validAndBeautyJsonValidProcessed,
            1,
            "String_",
        )
        self.assertRaises(
            TypeError,
            post_data_helper.validAndBeautyJsonValidProcessed,
            {"test": "test"},
            1,
        )

    def test_store_valid_and_beauty_json_valid(self):
        processed_measurement_json = {
            "CO": 1986.208,
            "CO_ug_m3": 1986.208,
            "H2S_ug_m3": 43.404,
            "H2S": 43.404,
            "NO2": 19.78,
            "NO2_ug_m3": 19.78,
            "O3": 3.126,
            "O3_ug_m3": 3.126,
            "VOC": 0,
            "CO2": 1,
            "SO2": 4.388,
            "SO2_ug_m3": 4.388,
            "PM10": 35.349,
            "PM25": 11.678,
            "UVA": 1,
            "UVB": 1,
            "alt": 0.0,
            "lat": -12.0402780000002,
            "lon": -77.0436090000003,
            "PM1": 1,
            "timestamp_zone": "Tue, 05 Jan 2021 05:00:00 GMT",
            "ID": "qH021",
            "timestamp": "Fri, 01 Jan 2021 00:00:00 GMT",
            "pressure": 10,
            "humidity": 25,
            "I_temperature": 25,
            "temperature": 21,
            "spl": 1,
            "UV": 1,
        }
        post_data_helper.validAndBeautyJsonValidProcessed(
            processed_measurement_json, "qH021", -1
        )

    def test_format_telemetry_for_storage_not_valid(self):
        self.assertRaises(
            TypeError, post_data_helper.formatTelemetryForStorage
        )
        self.assertRaises(
            TypeError, post_data_helper.formatTelemetryForStorage, True
        )
        self.assertRaises(
            TypeError, post_data_helper.formatTelemetryForStorage, -5.0
        )
        self.assertRaises(
            TypeError, post_data_helper.formatTelemetryForStorage, None
        )
        self.assertRaises(
            TypeError, post_data_helper.formatTelemetryForStorage, 1, "String_"
        )

    def test_format_telemetry_for_storage_valid(self):
        telemetry = {
            "lat": -12.0724959,
            "lon": -77.0823532,
            "alt": -0.05,
            "dist_home": 0.0,
            "airspeed": 0.02,
            "waypoint": None,
            "last_waypoint": False,
            "flight_mode": "MANUAL",
            "just_landed": False,
            "new_flight": False,
            "voltage": 12.59,
            "current": 0.0,
            "level": 100,
            "sonar_dist": None,
            "num_gps": 10,
            "fix_type": 6,
            "IRLOCK_status": False,
            "status_msg": "",
            "throttle": None,
            "rcout": None,
            "compass1": None,
            "compass2": None,
            "gps": None,
            "gps2": None,
            "vibrations": None,
            "ekf_status": None,
            "yaw": 358,
            "irlock": None,
        }
        telemetry_processed = {
            "airspeed": 0.02,
            "alt": -0.05,
            "battery_perc": 100,
            "dist_home": 0.0,
            "compass1_x": -1,
            "compass1_y": -1,
            "compass1_z": -1,
            "compass2_x": -1,
            "compass2_y": -1,
            "compass2_z": -1,
            "compass_variance": -1,
            "current": 0.0,
            "fix_type": 6,
            "flight_mode": "MANUAL",
            "gps_sats": -1,
            "gps_fix": -1,
            "gps2_sats": -1,
            "gps2_fix": -1,
            "irlock_x": -1,
            "irlock_y": -1,
            "irlock_status": False,
            "lat": -12.0724959,
            "lon": -77.0823532,
            "num_gps": 10,
            "pos_horiz_variance": -1,
            "pos_vert_variance": -1,
            "rcout1": -1,
            "rcout2": -1,
            "rcout3": -1,
            "rcout4": -1,
            "rcout5": -1,
            "rcout6": -1,
            "rcout7": -1,
            "rcout8": -1,
            "sonar_dist": None,
            "throttle": None,
            "vibrations_x": -1,
            "vibrations_y": -1,
            "vibrations_z": -1,
            "voltage": 12.59,
            "velocity_variance": -1,
            "terrain_alt_variance": -1,
            "waypoint": None,
            "yaw": 358,
        }
        self.assertAlmostEqual(
            post_data_helper.formatTelemetryForStorage(telemetry),
            telemetry_processed,
        )

    def test_store_logs_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.storeLogs)
        self.assertRaises(TypeError, post_data_helper.storeLogs, True)
        self.assertRaises(TypeError, post_data_helper.storeLogs, -5.0)
        self.assertRaises(TypeError, post_data_helper.storeLogs, None)
        self.assertRaises(TypeError, post_data_helper.storeLogs, 1, "String_")

    def test_store_logs_valid(self):
        drone_name = "qH057"
        telemetry = {
            "lat": -12.0724959,
            "lon": -77.0823532,
            "alt": -0.05,
            "dist_home": 0.0,
            "airspeed": 0.02,
            "waypoint": None,
            "last_waypoint": False,
            "flight_mode": "MANUAL",
            "just_landed": False,
            "new_flight": False,
            "voltage": 12.59,
            "current": 0.0,
            "level": 100,
            "sonar_dist": -1,
            "num_gps": 10,
            "fix_type": 6,
            "IRLOCK_status": False,
            "status_msg": "",
            "throttle": -1,
            "rcout": -1,
            "compass1": -1,
            "compass2": -1,
            "gps": -1,
            "gps2": -1,
            "vibrations": None,
            "ekf_status": -1,
            "yaw": 358,
            "irlock": -1,
        }
        post_data_helper.storeLogs(telemetry, drone_name)

    def test_record_drone_takeoff_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.recordDroneTakeoff)
        self.assertRaises(TypeError, post_data_helper.recordDroneTakeoff, True)
        self.assertRaises(TypeError, post_data_helper.recordDroneTakeoff, -5.0)
        self.assertRaises(TypeError, post_data_helper.recordDroneTakeoff, None)
        self.assertRaises(TypeError, post_data_helper.recordDroneTakeoff, 1, 2)

    def test_record_drone_landing_not_valid(self):
        self.assertRaises(TypeError, post_data_helper.recordDroneLanding)
        self.assertRaises(TypeError, post_data_helper.recordDroneLanding, True)
        self.assertRaises(TypeError, post_data_helper.recordDroneLanding, -5.0)
        self.assertRaises(TypeError, post_data_helper.recordDroneLanding, None)

    def test_record_drone_flight_valid(self):
        drone_name = "qH057"
        flight_start = datetime.datetime.now(dateutil.tz.tzutc())
        flight_end = datetime.datetime.now(
            dateutil.tz.tzutc()
        ) + datetime.timedelta(minutes=15)
        flight_detail = "Good flight"
        post_data_helper.recordDroneTakeoff(flight_start, drone_name)
        post_data_helper.recordDroneLanding(
            flight_end, drone_name, flight_detail
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
