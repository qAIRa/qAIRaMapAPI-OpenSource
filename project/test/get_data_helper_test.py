import datetime
import unittest
from datetime import timedelta

import dateutil
import dateutil.parser
import pytz

import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper


class TestGetDataHelper(unittest.TestCase):
    """Test of Get Data Functions"""

    def test_query_air_valid_quality_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryDBValidAirQuality)
        self.assertRaises(
            TypeError, get_data_helper.queryDBValidAirQuality, {"qhawax_id": 5}
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBValidAirQuality, True
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBValidAirQuality, -5.0
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBValidAirQuality, None
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBValidAirQuality, "qH001", 1
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBValidAirQuality,
            "qH001",
            "2020/01/01",
        )

    def test_query_air_valid_quality_valid(self):
        initial_timestamp = "02-09-2020 00:00:00"
        last_timestamp = "02-09-2020 05:01:00"
        self.assertAlmostEqual(
            get_data_helper.queryDBValidAirQuality(
                1, initial_timestamp, last_timestamp
            ),
            [],
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBValidAirQuality(
                100, initial_timestamp, last_timestamp
            ),
            None,
        )

    def test_query_gas_average_measurement_not_valid(self):
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasAverageMeasurement
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBGasAverageMeasurement,
            {"qhawax_id": 5},
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasAverageMeasurement, True
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasAverageMeasurement, -5.0
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasAverageMeasurement, None
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBGasAverageMeasurement,
            "qH001",
            1,
            2,
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasAverageMeasurement, "qH001", 1
        )
        self.assertRaises(
            ValueError,
            get_data_helper.queryDBGasAverageMeasurement,
            "qH001",
            "H2O",
        )

    def test_query_gas_average_measurement_valid(self):
        qhawax = "qH057"
        naive_time1 = datetime.time(0, 0, 0)
        naive_time2 = datetime.time(1, 0, 0)
        naive_time3 = datetime.time(2, 0, 0)
        naive_time4 = datetime.time(4, 0, 0)
        date = datetime.date(2021, 1, 6)
        naive_datetime1 = datetime.datetime.combine(date, naive_time1)
        naive_datetime2 = datetime.datetime.combine(date, naive_time2)
        naive_datetime3 = datetime.datetime.combine(date, naive_time3)
        naive_datetime4 = datetime.datetime.combine(date, naive_time4)
        timezone = pytz.timezone("UTC")
        aware_datetime1 = timezone.localize(naive_datetime1)
        aware_datetime2 = timezone.localize(naive_datetime2)
        aware_datetime3 = timezone.localize(naive_datetime3)
        aware_datetime4 = timezone.localize(naive_datetime4)
        co = [(aware_datetime1, 1986.208), (aware_datetime4, 1986.208)]
        h2s = [(aware_datetime1, 43.404), (aware_datetime4, 43.404)]
        no2 = [(aware_datetime1, 19.78), (aware_datetime4, 19.78)]
        o3 = [(aware_datetime1, 3.126), (aware_datetime4, 3.126)]
        so2 = [(aware_datetime1, 4.388), (aware_datetime4, 4.388)]
        pm25 = [(aware_datetime1, 11.678), (aware_datetime4, 11.678)]
        pm10 = [(aware_datetime1, 35.349), (aware_datetime4, 35.349)]
        co_format = [
            {"timestamp_zone": aware_datetime1, "sensor": 1986.208},
            {"timestamp_zone": aware_datetime2, "sensor": ""},
            {"timestamp_zone": aware_datetime3, "sensor": ""},
            {"timestamp_zone": aware_datetime4, "sensor": 1986.208},
        ]
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"CO"))
        # print(util_helper.getFormatData(get_data_helper.queryDBGasAverageMeasurement(qhawax,"CO")))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"H2S"))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"NO2"))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"O3"))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM25"))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"PM10"))
        # print(get_data_helper.queryDBGasAverageMeasurement(qhawax,"SO2"))

        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "CO"), []
        )
        self.assertAlmostEqual(
            util_helper.getFormatData(
                get_data_helper.queryDBGasAverageMeasurement("qH057", "CO")
            ),
            [],
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "H2S"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "NO2"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "O3"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "PM25"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "PM10"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement(qhawax, "SO2"), []
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBGasAverageMeasurement("qH100", "CO"), None
        )

    def test_query_valid_air_quality_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryDBGasInca)
        self.assertRaises(
            TypeError, get_data_helper.queryDBGasInca, {"qhawax_id": 5}
        )
        self.assertRaises(TypeError, get_data_helper.queryDBGasInca, True)
        self.assertRaises(TypeError, get_data_helper.queryDBGasInca, -5.0)
        self.assertRaises(TypeError, get_data_helper.queryDBGasInca, None)
        self.assertRaises(TypeError, get_data_helper.queryDBGasInca, "qH001")
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBGasInca,
            1,
            "02-09-2010 00:01:00",
            "%d-%m-%Y %H:%M:%S",
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBGasInca,
            "02-09-2010 00:01:00",
            1,
            "%d-%m-%Y %H:%M:%S",
        )

    def test_query_valid_air_quality_valid(self):
        initial_timestamp = "02-09-2010 00:00:00"
        last_timestamp = "02-09-2010 00:01:00"
        self.assertAlmostEqual(
            get_data_helper.queryDBGasInca(initial_timestamp, last_timestamp),
            [],
        )

    def test_query_processed_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryDBProcessed)
        self.assertRaises(
            TypeError, get_data_helper.queryDBProcessed, {"qhawax_id": 5}
        )
        self.assertRaises(TypeError, get_data_helper.queryDBProcessed, True)
        self.assertRaises(TypeError, get_data_helper.queryDBProcessed, -5.0)
        self.assertRaises(TypeError, get_data_helper.queryDBProcessed, None)
        self.assertRaises(
            TypeError, get_data_helper.queryDBProcessed, "qH001", 1
        )
        self.assertRaises(
            TypeError, get_data_helper.queryDBProcessed, "qH001", ""
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBProcessed,
            "qH001",
            1,
            "02-09-2010 00:01:00",
            "%d-%m-%Y %H:%M:%S",
        )
        self.assertRaises(
            TypeError,
            get_data_helper.queryDBProcessed,
            "qH001",
            "02-09-2010 00:01:00",
            1,
            "%d-%m-%Y %H:%M:%S",
        )

    def test_query_processed_valid(self):
        naive_time = datetime.time(5, 0, 21)
        date = datetime.date(2020, 12, 20)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        initial_timestamp = timezone.localize(naive_datetime)
        date = datetime.date(2020, 12, 21)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        last_timestamp = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            get_data_helper.queryDBProcessed(
                "qH057", initial_timestamp, last_timestamp
            ),
            [],
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBProcessed(
                "qH100", initial_timestamp, last_timestamp
            ),
            None,
        )

        # date = datetime.date(2021, 3, 24)

        # naive_time = datetime.time(5,5,8)
        # naive_datetime = datetime.datetime.combine(date, naive_time)
        # timezone = pytz.timezone('UTC')
        # initial_timestamp = timezone.localize(naive_datetime)

        # naive_time = datetime.time(17,3,8)
        # naive_datetime = datetime.datetime.combine(date, naive_time)
        # timezone = pytz.timezone('UTC')
        # last_timestamp = timezone.localize(naive_datetime)

        # data_processed = [{'CO': 733.85, 'CO2': None, 'H2S': 9.653, 'NO': None, 'NO2': 26.762, 'O3': 12.89,
        # 		 'PM1': 3.814, 'PM25': 10.746, 'PM10': 52.494, 'SO2': 6.682, 'VOC': None, 'UV': 0.0,
        # 		 'UVA': 0.0, 'UVB': None, 'spl': 75.7, 'humidity': 99.9, 'pressure': 9.891, 'temperature': 23.9,
        # 		 'lat': -12.072736, 'lon': -77.082687, 'alt': None, 'SO2_ug_m3': 17.507, 'I_temperature': 26.8,
        # 		 'CO_ug_m3': 843.928, 'H2S_ug_m3': 13.418, 'NO2_ug_m3': 50.313, 'O3_ug_m3': 25.264}]
        # data = get_data_helper.queryDBProcessed("qH021", initial_timestamp, last_timestamp)
        # data.pop('timestamp_zone', None)
        # self.assertAlmostEqual(data,data_processed)

    def test_query_last_main_inca_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryLastMainInca)
        self.assertRaises(
            TypeError, get_data_helper.queryLastMainInca, {"qhawax_id": 5}
        )
        self.assertRaises(TypeError, get_data_helper.queryLastMainInca, True)
        self.assertRaises(TypeError, get_data_helper.queryLastMainInca, -5.0)
        self.assertRaises(TypeError, get_data_helper.queryLastMainInca, None)
        self.assertRaises(TypeError, get_data_helper.queryLastMainInca, 1)

    def test_query_last_main_inca_valid(self):
        self.assertAlmostEqual(
            get_data_helper.queryLastMainInca("qH058"), None
        )
        self.assertAlmostEqual(
            get_data_helper.queryLastMainInca("qH004"), 50.0
        )
        self.assertAlmostEqual(
            get_data_helper.queryLastMainInca("qH100"), None
        )

    def test_query_first_timestamp_valid_not_valid(self):
        self.assertRaises(
            TypeError, get_data_helper.getFirstTimestampValidProcessed
        )
        self.assertRaises(
            TypeError,
            get_data_helper.getFirstTimestampValidProcessed,
            {"qhawax_id": 5},
        )
        self.assertRaises(
            TypeError, get_data_helper.getFirstTimestampValidProcessed, True
        )
        self.assertRaises(
            TypeError, get_data_helper.getFirstTimestampValidProcessed, -5.0
        )
        self.assertRaises(
            TypeError, get_data_helper.getFirstTimestampValidProcessed, None
        )

    def test_query_first_timestamp_valid_valid(self):
        naive_time = datetime.time(5, 0, 0)
        date = datetime.date(2021, 1, 5)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        aware_datetime = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            get_data_helper.getFirstTimestampValidProcessed(307),
            aware_datetime,
        )
        self.assertAlmostEqual(
            get_data_helper.getFirstTimestampValidProcessed(100), None
        )

    def test_get_qhawax_latest_timestamp_processed_measurement_not_valid(self):
        self.assertRaises(
            TypeError,
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement,
        )
        self.assertRaises(
            TypeError,
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement,
            {"qhawax_id": 5},
        )
        self.assertRaises(
            TypeError,
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement,
            True,
        )
        self.assertRaises(
            TypeError,
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement,
            -5.0,
        )
        self.assertRaises(
            TypeError,
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement,
            None,
        )

    def test_get_qhawax_latest_timestamp_processed_measurement_valid(self):
        naive_time = datetime.time(0, 0, 0)
        date = datetime.date(2021, 1, 4)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        aware_datetime = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement(
                "qH057"
            ),
            aware_datetime,
        )
        self.assertAlmostEqual(
            get_data_helper.getQhawaxLatestTimestampProcessedMeasurement(
                "qH001"
            ),
            None,
        )

    def test_all_qhawax_is_in_flight_valid(self):
        self.assertAlmostEqual(get_data_helper.AllqHAWAXIsInFlight(), [])

    def test_qhawax_is_in_flight_valid(self):
        self.assertAlmostEqual(get_data_helper.qHAWAXIsInFlight("qH057"), None)

    def test_query_db_processed_by_pollutant_valid(self):
        naive_time = datetime.time(5, 0, 0)
        date = datetime.date(2021, 3, 22)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        initial_timestamp = timezone.localize(naive_datetime)

        date = datetime.date(2021, 3, 23)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        last_timestamp = timezone.localize(naive_datetime)

        self.assertAlmostEqual(
            get_data_helper.queryDBProcessedByPollutant(
                "qH057", initial_timestamp, last_timestamp, "NO2"
            ),
            [],
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBProcessedByPollutant(
                "qH756", initial_timestamp, last_timestamp, "NO2"
            ),
            None,
        )

    def test_query_flights_filter_by_time_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryFlightsFilterByTime)
        self.assertRaises(
            TypeError,
            get_data_helper.queryFlightsFilterByTime,
            {"qhawax_id": 5},
        )
        self.assertRaises(
            TypeError, get_data_helper.queryFlightsFilterByTime, True
        )
        self.assertRaises(
            TypeError, get_data_helper.queryFlightsFilterByTime, -5.0
        )

    def test_query_flights_filter_by_time_valid(self):
        naive_time = datetime.time(5, 0, 0)
        date = datetime.date(2021, 3, 22)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        initial_timestamp = timezone.localize(naive_datetime)

        date = datetime.date(2021, 3, 23)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        last_timestamp = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            get_data_helper.queryFlightsFilterByTime(
                initial_timestamp, last_timestamp
            ),
            [],
        )

    def test_query_telemetry_not_valid(self):
        self.assertRaises(TypeError, get_data_helper.queryDBTelemetry)
        self.assertRaises(
            TypeError, get_data_helper.queryDBTelemetry, {"qhawax_id": 5}
        )
        self.assertRaises(TypeError, get_data_helper.queryDBTelemetry, True)
        self.assertRaises(TypeError, get_data_helper.queryDBTelemetry, -5.0)

    def test_query_telemetry_valid(self):
        naive_time = datetime.time(5, 0, 0)
        date = datetime.date(2021, 3, 22)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        initial_timestamp = timezone.localize(naive_datetime)

        date = datetime.date(2021, 3, 23)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        last_timestamp = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            get_data_helper.queryDBTelemetry(
                "qH006", initial_timestamp, last_timestamp
            ),
            [],
        )
        self.assertAlmostEqual(
            get_data_helper.queryDBTelemetry(
                "qH001", initial_timestamp, last_timestamp
            ),
            None,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
