import datetime
import unittest
from datetime import timedelta

import dateutil
import dateutil.parser
import pytz

import project.main.data.get_data_helper as get_data_helper
import project.main.util_helper as util_helper


class TestUtilHelper(unittest.TestCase):
    """
    Test of Util Helper Functions

    """

    def test_valid_time_json_processed_not_valid(self):
        self.assertRaises(TypeError, util_helper.validTimeJsonProcessed)
        self.assertRaises(
            TypeError, util_helper.validTimeJsonProcessed, "resultado"
        )
        self.assertRaises(TypeError, util_helper.validTimeJsonProcessed, None)
        self.assertRaises(TypeError, util_helper.validTimeJsonProcessed, 50)

    def test_valid_time_json_processed_valid(self):
        data_json_current_year = {"timestamp": "2020-09-01"}
        data_json_future = {"timestamp": "2080-09-01"}
        var_datetime = (
            datetime.datetime.now(dateutil.tz.tzutc())
            - datetime.timedelta(hours=5)
        ).strftime("%Y-%m-%d %H:%M:%S")
        datetime_zone = (datetime.datetime.now(dateutil.tz.tzutc())).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data_json_future_fix = {
            "timestamp": var_datetime,
            "timestamp_zone": datetime_zone,
        }
        self.assertAlmostEqual(
            util_helper.validTimeJsonProcessed(data_json_current_year),
            data_json_current_year,
        )
        self.assertAlmostEqual(
            util_helper.validTimeJsonProcessed(data_json_future),
            data_json_future_fix,
        )

    def test_valid_and_beauty_json_processed_not_valid(self):
        self.assertRaises(TypeError, util_helper.validAndBeautyJsonProcessed)
        self.assertRaises(
            TypeError, util_helper.validAndBeautyJsonProcessed, "resultado"
        )
        self.assertRaises(
            TypeError, util_helper.validAndBeautyJsonProcessed, None
        )
        self.assertRaises(
            TypeError, util_helper.validAndBeautyJsonProcessed, 50
        )

    def test_valid_and_beauty_json_processed_valid(self):
        data = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": 1.15,
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": 1,
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 100,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "timestamp_zone": "2020-01-01 00:00:00",
            "VOC": 1,
        }
        data_without = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": 1.15,
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": 1,
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 100,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "VOC": 1,
        }
        data_pressure = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": 1.15,
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": 1,
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 1.0,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "timestamp_zone": "2020-01-01 00:00:00",
            "VOC": 1,
            "CO2": None,
            "I_temperature": None,
        }
        self.assertAlmostEqual(
            util_helper.validAndBeautyJsonProcessed(data), data_pressure
        )
        self.assertAlmostEqual(
            util_helper.validAndBeautyJsonProcessed(data_without),
            data_pressure,
        )

    def test_gas_conversion_ppb_to_mg_not_valid(self):
        self.assertRaises(TypeError, util_helper.gasConversionPPBtoMG, 5, 5)
        self.assertRaises(
            TypeError, util_helper.gasConversionPPBtoMG, {"hola": "hola"}, 5
        )
        self.assertRaises(
            TypeError, util_helper.gasConversionPPBtoMG, 5, [5, 4, 3]
        )

    def test_gas_conversion_ppb_to_mg_valid(self):
        data = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": 1.15,
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": 1,
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 100,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "timestamp_zone": "2020-01-01 00:00:00",
            "VOC": None,
            "CO2": None,
            "I_temperature": None,
        }
        arr_season = [2.62, 1.88, 1.96, 1.15, 1.39]
        self.assertAlmostEqual(
            util_helper.gasConversionPPBtoMG(data, arr_season), data
        )

    def test_round_up_three_not_valid(self):
        self.assertRaises(TypeError, util_helper.roundUpThree)
        self.assertRaises(TypeError, util_helper.roundUpThree, 5)
        self.assertRaises(TypeError, util_helper.roundUpThree, "resultado")
        self.assertRaises(TypeError, util_helper.roundUpThree, None)
        self.assertRaises(TypeError, util_helper.roundUpThree, True)

    def test_round_up_three_valid(self):
        y = {
            "ID": "qH004",
            "CO": 162.3791119,
            "CO_ug_m3": 186.787111,
            "H2S": 0,
            "H2S_ug_m3": 1.42111,
            "NO2": 1.218,
            "NO2_ug_m3": 2.28111,
            "O3": 0,
            "O3_ug_m3": 29.12311,
            "PM1": 0,
            "PM10": 0,
            "PM25": 0,
            "SO2": 0.77,
            "SO2_ug_m3": 2.055551,
            "spl": 0,
            "UV": 1.0,
            "UVA": 0,
            "UVB": 0,
            "humidity": 71.9,
            "lat": -12.072736,
            "lon": -77.082687,
            "pressure": 100743.24,
            "temperature": 19.1,
            "timestamp": "2020-08-31 00:00:00.0-05:00",
        }
        last_y = {
            "ID": "qH004",
            "CO": 162.379,
            "CO_ug_m3": 186.787,
            "H2S": 0,
            "H2S_ug_m3": 1.421,
            "NO2": 1.218,
            "NO2_ug_m3": 2.281,
            "O3": 0,
            "O3_ug_m3": 29.123,
            "PM1": 0,
            "PM10": 0,
            "PM25": 0,
            "SO2": 0.77,
            "SO2_ug_m3": 2.056,
            "spl": 0,
            "UV": 1.0,
            "UVA": 0,
            "UVB": 0,
            "humidity": 71.9,
            "lat": -12.072736,
            "lon": -77.082687,
            "pressure": 100743.24,
            "temperature": 19.1,
            "timestamp": "2020-08-31 00:00:00.0-05:00",
        }
        self.assertAlmostEqual(util_helper.roundUpThree(y), last_y)

    def test_check_number_values_not_valid(self):
        self.assertRaises(TypeError, util_helper.checkNumberValues)
        self.assertRaises(TypeError, util_helper.checkNumberValues, 5)
        self.assertRaises(
            TypeError, util_helper.checkNumberValues, "resultado"
        )
        self.assertRaises(TypeError, util_helper.checkNumberValues, None)
        self.assertRaises(TypeError, util_helper.checkNumberValues, True)

    def test_check_number_values_valid(self):
        y = {
            "ID": "qH004",
            "timestamp": "2020-08-31 00:00:00.0-05:00",
            "lat": -12.072736,
            "lon": -77.082687,
            "CO": 162.379,
            "H2S": 0,
            "NO2": 1.218,
            "O3": 0,
            "SO2": 0.77,
            "PM1": 0,
            "PM25": 0,
            "PM10": 0,
            "UV": "Nan",
            "UVA": "Nan",
            "UVB": "Nan",
            "spl": 0,
            "temperature": 19.1,
            "pressure": 100743.24,
            "humidity": 71.9,
        }
        self.assertAlmostEqual(util_helper.checkNumberValues(y), y)

    def test_are_fields_correct_not_valid(self):
        self.assertRaises(TypeError, util_helper.areFieldsValid)
        self.assertRaises(TypeError, util_helper.areFieldsValid, 5)
        self.assertRaises(TypeError, util_helper.areFieldsValid, "resultado")
        self.assertRaises(TypeError, util_helper.areFieldsValid, None)
        self.assertRaises(TypeError, util_helper.areFieldsValid, True)

    def test_get_format_data_not_valid(self):
        self.assertRaises(TypeError, util_helper.getFormatData)
        self.assertRaises(TypeError, util_helper.getFormatData, 5)
        self.assertRaises(TypeError, util_helper.getFormatData, "year")
        self.assertRaises(TypeError, util_helper.getFormatData, -1, 1)
        self.assertRaises(TypeError, util_helper.getFormatData, True)

    def test_get_format_data_valid(self):
        gas_average_measurement = None
        self.assertAlmostEqual(
            util_helper.getFormatData(gas_average_measurement), None
        )
        gas_average_measurement = get_data_helper.queryDBGasAverageMeasurement(
            "qH021", "NO2"
        )
        gas_average_measurement = util_helper.getFormatData(
            gas_average_measurement
        )

    def test_set_none_string_elements_not_valid(self):
        self.assertRaises(TypeError, util_helper.setNoneStringElements, "test")
        self.assertRaises(TypeError, util_helper.setNoneStringElements, 54)
        self.assertRaises(
            TypeError, util_helper.setNoneStringElements, [5, 4, 3]
        )

    def test_set_none_string_elements_valid(self):
        data = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": "string",
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": "string",
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 100,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "timestamp_zone": "2020-01-01 00:00:00",
            "VOC": None,
            "CO2": None,
            "I_temperature": None,
        }
        processed = {
            "ID": 1,
            "CO": 1,
            "CO_ug_m3": None,
            "H2S": 1,
            "H2S_ug_m3": 1.39,
            "NO2": None,
            "NO2_ug_m3": 1.88,
            "O3": 1,
            "O3_ug_m3": 1.96,
            "PM1": 1,
            "PM10": 1,
            "PM25": 1,
            "SO2": 1,
            "SO2_ug_m3": 2.62,
            "spl": 1,
            "UV": 1,
            "UVA": 1,
            "UVB": 1,
            "humidity": 1,
            "lat": -12.000000,
            "lon": -77.00000,
            "pressure": 100,
            "temperature": 20,
            "timestamp": "2020-01-01 00:00:00",
            "timestamp_zone": "2020-01-01 00:00:00",
            "VOC": None,
            "CO2": None,
            "I_temperature": None,
        }
        self.assertAlmostEqual(
            util_helper.setNoneStringElements(data), processed
        )

    def test_beauty_format_date_not_valid(self):
        self.assertRaises(
            TypeError, util_helper.beautyFormatDate, {"test": "test"}, 5
        )

    def test_beauty_format_date_valid(self):
        naive_time = datetime.time(19, 7, 7)
        date = datetime.date(2021, 1, 20)
        naive_datetime = datetime.datetime.combine(date, naive_time)
        timezone = pytz.timezone("UTC")
        aware_datetime = timezone.localize(naive_datetime)
        self.assertAlmostEqual(
            util_helper.beautyFormatDate(aware_datetime), "20-01-2021 19:07:07"
        )

    def test_add_zero_not_valid(self):
        self.assertRaises(TypeError, util_helper.addZero, {"test": "test"}, 5)
        self.assertRaises(TypeError, util_helper.addZero, [5, 4, 3])
        self.assertRaises(TypeError, util_helper.addZero, "test")

    def test_add_zero_valid(self):
        self.assertAlmostEqual(util_helper.addZero(5), "05")
        self.assertAlmostEqual(util_helper.addZero(20), "20")


if __name__ == "__main__":
    unittest.main(verbosity=2)
