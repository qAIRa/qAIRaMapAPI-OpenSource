import datetime

import dateutil
import dateutil.parser

import project.main.business.get_business_helper as get_business_helper
import project.main.data.get_data_helper as get_data_helper
import project.main.exceptions as exceptions
import project.main.same_function_helper as same_helper
import project.main.util_helper as util_helper
from project import app, db
from project.database.models import (Bitacora, Company, EcaNoise, Qhawax,
                                     QhawaxInstallationHistory)

session = db.session
now = datetime.datetime.now(dateutil.tz.tzutc())


def updateMainIncaQhawaxTable(new_main_inca, qhawax_name):
    """Helper qHAWAX function to save main inca value in qHAWAX table"""
    new_main_inca = exceptions.checkVariable_helper(new_main_inca, int)
    qhawax_json_main_inca = {"main_inca": new_main_inca}
    same_helper.qhawaxQueryUpdateFilterByQhawaxName(
        qhawax_json_main_inca, qhawax_name
    )


def saveStatusQhawaxTable(qhawax_name, qhawax_status, main_inca):
    """Set qHAWAX ON or OFF in qHAWAX table"""
    main_inca = exceptions.checkVariable_helper(main_inca, int)
    qhawax_status = exceptions.checkVariable_helper(qhawax_status, str)
    qhawax_json_status = {"state": qhawax_status, "main_inca": main_inca}
    same_helper.qhawaxQueryUpdateFilterByQhawaxName(
        qhawax_json_status, qhawax_name
    )


def setAvailabilityQhawax(qhawax_name, availability):
    """Update qHAWAX Availability to Occupied or Free"""
    availability = exceptions.checkVariable_helper(availability, str)
    qhawax_json_availability = {"availability": availability}
    same_helper.qhawaxQueryUpdateFilterByQhawaxName(
        qhawax_json_availability, qhawax_name
    )


def changeMode(qhawax_name, mode):
    """Change To Other Mode"""
    mode = exceptions.checkVariable_helper(mode, str)
    qhawax_json_mode = {"mode": mode}
    same_helper.qhawaxQueryUpdateFilterByQhawaxName(
        qhawax_json_mode, qhawax_name
    )


def updateMainIncaQhawaxInstallationTable(new_main_inca, qhawax_name):
    """Helper qHAWAX function to save main inca value in qHAWAX Installation table"""
    new_main_inca = exceptions.checkVariable_helper(new_main_inca, int)
    qhawax_json_main_inca_installation = {"main_inca": new_main_inca}
    same_helper.qhawaxInstallationQueryUpdate(
        qhawax_json_main_inca_installation, qhawax_name
    )


def saveStatusOffQhawaxInstallationTable(qhawax_name, time):
    """Set qHAWAX OFF in qHAWAX Installation table"""
    qhawax_json_status_off = {
        "main_inca": -1,
        "last_registration_time_zone": time,
    }
    same_helper.qhawaxInstallationQueryUpdate(
        qhawax_json_status_off, qhawax_name
    )


def saveTurnOnLastTime(qhawax_name):
    """Set qHAWAX ON in qHAWAX Installation table"""
    now2 = datetime.datetime.now(dateutil.tz.tzutc())
    qhawax_json_on = {
        "main_inca": 0,
        "last_time_physically_turn_on_zone": now2.replace(tzinfo=None),
    }
    same_helper.qhawaxInstallationQueryUpdate(qhawax_json_on, qhawax_name)


def saveTurnOnLastTimeProcessedMobile(qhawax_name):
    """Updates last_time_physically_turn_on_zone based on last registration time zone"""
    latest_turn_off = get_business_helper.queryLastRegistrationTimezone(
        qhawax_name
    )
    if not (latest_turn_off == None or latest_turn_off == []):
        now2 = datetime.datetime.now(dateutil.tz.tzutc())
        difference = now2 - latest_turn_off
        seconds_interval = 1800
        if seconds_interval < int(
            difference.total_seconds()
        ):  # if reconnection takes longer than 30 minutes, we update the last_turn_on
            # every reconnection longer than 30 mins, includes the ones that last longer than a day so they should not be an issue
            qhawax_json_on = {
                "main_inca": 0,
                "last_time_physically_turn_on_zone": now2.replace(tzinfo=None),
            }
            same_helper.qhawaxInstallationQueryUpdate(
                qhawax_json_on, qhawax_name
            )

        trip_start, trip_id = get_data_helper.getqHAWAXMobileLatestTripStart(
            qhawax_name
        )
        if trip_id != None and trip_start != None:
            # trip_start = datetime.datetime.strptime('2021-07-12 12:00:00', '%Y-%m-%d %H:%M:%S') # test
            date_start = (
                trip_start - datetime.timedelta(hours=5)
            ).date()  # local
            now_date = (
                datetime.datetime.now(dateutil.tz.tzutc())
                - datetime.timedelta(hours=5)
            ).date()
            if date_start == now_date:
                same_helper.setTripEndNull(trip_id)


def turnOnAfterCalibration(qhawax_name):
    """Set qHAWAX ON in qHAWAX Installation table"""
    now2 = datetime.datetime.now(dateutil.tz.tzutc())
    qhawax_json_on_after_calibration = {
        "last_time_physically_turn_on_zone": now2.replace(tzinfo=None)
    }
    same_helper.qhawaxInstallationQueryUpdate(
        qhawax_json_on_after_calibration, qhawax_name
    )


def saveEndWorkFieldDate(qhawax_name, end_date):
    """Save End Work in Field"""
    qhawax_json_end_field = {"end_date_zone": end_date}
    same_helper.qhawaxInstallationQueryUpdate(
        qhawax_json_end_field, qhawax_name
    )


def updateTimeOffWithLastTurnOff(time_turn_off_binnacle, qhawax_name):
    qhawax_json_last_turn_off = {
        "last_registration_time_zone": time_turn_off_binnacle
    }
    same_helper.qhawaxInstallationQueryUpdate(
        qhawax_json_last_turn_off, qhawax_name
    )


def updateTimeOnPreviousTurnOn(qhawax_name, mins):
    MINUTES_ALLOWED = 240
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if installation_id is not None:
        turn_on = (
            get_data_helper.getQhawaxLatestTimestampValidProcessedMeasurement(
                qhawax_name
            )
        )
        # what if the turn_on is very recent? does not matter as long as there a value
        now = datetime.datetime.now(dateutil.tz.tzutc())
        if turn_on != None:
            minutes_difference = int((now - turn_on).total_seconds() / 60)
            # if(minutes_difference>=)
            turn_off = turn_on - datetime.timedelta(minutes=mins)
            session.query(QhawaxInstallationHistory).filter_by(
                id=installation_id
            ).update(values={"last_registration_time_zone": turn_off})
            session.commit()
        else:
            turn_on = datetime.datetime.now(
                dateutil.tz.tzutc()
            ) - datetime.timedelta(minutes=120 - mins)
            turn_off = datetime.datetime.now(
                dateutil.tz.tzutc()
            ) - datetime.timedelta(minutes=120)
            session.query(QhawaxInstallationHistory).filter_by(
                id=installation_id
            ).update(
                values={
                    "last_time_physically_turn_on_zone": turn_on,
                    "last_registration_time_zone": turn_off,
                }
            )
            session.commit()


def updateLastLocation(qhawax_name, location):
    """Helper Drone Log function to update location of andean drone in qHAWAX Installation table"""
    location = exceptions.checkVariable_helper(location, dict)
    same_helper.qhawaxInstallationQueryUpdate(location, qhawax_name)


def updateQhawaxInstallation(data):
    """Update qHAWAX in Field"""
    data = exceptions.checkVariable_helper(data, dict)
    if util_helper.areFieldsValid(data) == False:
        raise Exception("qHAWAX Installation fields must have data")

    data["qhawax_id"] = same_helper.getQhawaxID(data["qhawax_name"])
    data.pop("qhawax_name", None)
    session.query(QhawaxInstallationHistory).filter_by(
        qhawax_id=data["qhawax_id"],
        company_id=data["company_id"],
        end_date_zone=None,
    ).update(values=data)
    session.commit()


def util_qhawax_installation_set_up(
    qhawax_name, availability, mode, description, person_in_charge
):
    """qHAWAX Installation to set functions"""
    setAvailabilityQhawax(qhawax_name, availability)
    changeMode(qhawax_name, mode)
    writeBinnacle(qhawax_name, description, person_in_charge)


def resetOnLoop(qhawax_name, loop):
    """qHAWAX function to reset loop"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        json_loop = {"on_loop": loop}
        same_helper.qhawaxQueryUpdateFilterByQhawaxId(json_loop, qhawax_id)


def recordFirstTimeLoop(qhawax_name, timestamp):
    """qHAWAX function to record first time loop"""
    qhawax_id = same_helper.getQhawaxID(qhawax_name)
    if qhawax_id is not None:
        json_first_time_loop = {"first_time_loop": timestamp}
        same_helper.qhawaxQueryUpdateFilterByQhawaxId(
            json_first_time_loop, qhawax_id
        )


def setLastMeasurementOfQhawax(qH_name):
    """qHAWAX function to update last measurement"""
    last_main_inca_value = get_data_helper.queryLastMainInca(qH_name)
    if last_main_inca_value != None:
        updateMainIncaQhawaxInstallationTable(
            int(last_main_inca_value), qH_name
        )
        updateMainIncaQhawaxTable(int(last_main_inca_value), qH_name)
    last_time_of_turn_off_binnacle = get_business_helper.queryLastTimeOffDueLackEnergy(
        qH_name
    )  # query of the timestamp of the last description with "qHAWAX off" made by the API
    if last_time_of_turn_off_binnacle != None:
        updateTimeOffWithLastTurnOff(last_time_of_turn_off_binnacle, qH_name)


def createQhawax(qhawax_name, qhawax_type):
    """Create a qHAWAX module"""
    qhawax_name = exceptions.checkVariable_helper(qhawax_name, str)
    qhawax_type = exceptions.checkVariable_helper(qhawax_type, str)
    qhawax_data = {
        "name": qhawax_name,
        "qhawax_type": qhawax_type,
        "state": "OFF",
        "availability": "Available",
        "main_aqi": -1.0,
        "mode": "Stand By",
        "on_loop": 0,
        "main_inca": -1.0,
    }
    qhawax_data_var = Qhawax(**qhawax_data)
    session.add(qhawax_data_var)
    session.commit()


def createCompany(json_company):
    """Create a new company"""
    json_company = exceptions.checkVariable_helper(json_company, dict)
    company_name = json_company.pop("company_name", None)
    json_company["name"] = company_name
    company_var = Company(**json_company)
    session.add(company_var)
    session.commit()


def storeNewQhawaxInstallation(data):
    """Insert new qHAWAX in Field"""
    data = exceptions.checkVariable_helper(data, dict)
    if util_helper.areFieldsValid(data) == False:
        raise Exception("qHAWAX Installation fields have to have data")

    qhawax_id = same_helper.getQhawaxID(data["qhawax_name"])
    if qhawax_id != None:
        data["qhawax_id"] = int(qhawax_id)
        data["main_inca"] = same_helper.getMainIncaQhawaxTable(
            data["qhawax_name"]
        )
        data["installation_date_zone"] = data["instalation_date"]
        data["last_time_physically_turn_on_zone"] = data["instalation_date"]
        data.pop("instalation_date", None)
        data.pop("qhawax_name", None)
        if "id" in data:
            data.pop("id", None)
        if "company_name" in data:
            data.pop("company_name", None)
        qhawax_installation = QhawaxInstallationHistory(**data)
        session.add(qhawax_installation)
        session.commit()


def writeBinnacle(qhawax_name, description, person_in_charge):
    """Insert observations in Binnacle"""
    description = exceptions.checkVariable_helper(description, str)
    person_in_charge = exceptions.checkVariable_helper(person_in_charge, str)
    qHAWAX_ID = same_helper.getQhawaxID(qhawax_name)
    if qHAWAX_ID is not None:
        now2 = datetime.datetime.now(dateutil.tz.tzutc())
        bitacora = {
            "timestamp_zone": now2,
            "observation_type": "Interna",
            "description": description,
            "qhawax_id": qHAWAX_ID,
            "solution": None,
            "person_in_charge": person_in_charge,
            "end_date_zone": None,
            "start_date_zone": None,
        }
        bitacora_update = Bitacora(**bitacora)
        session.add(bitacora_update)
        session.commit()


def saveTimeQhawaxOff(qhawax_name):
    """Save time qHAWAX off with timestamp in UTC 0"""
    installation_id = same_helper.getInstallationIdBaseName(qhawax_name)
    if installation_id != None:
        session.query(QhawaxInstallationHistory).filter_by(
            id=installation_id
        ).update(
            values={
                "last_registration_time_zone": datetime.datetime.now(
                    dateutil.tz.tzutc()
                )
            }
        )
        session.commit()
