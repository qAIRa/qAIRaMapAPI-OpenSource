"""
Data shared by all test cases
"""
import datetime

from project import db
from project.database.models import (
    Company,
    EcaNoise,
    GasInca,
    ProcessedMeasurement,
    Qhawax,
    QhawaxInstallationHistory,
)


now = datetime.datetime.now()
today_midnight = datetime.datetime(now.year, now.month, now.day)

company_data = {
    "name": "qAIRa",
    "email_group": "qairadrones.com",
    "ruc": "20600763491",
    "address": "Test Address",
    "phone": "000000000",
    "contact_person": "Test Person",
}
company = Company(**company_data)
db.session.add(company)
db.session.commit()

eca_noise = EcaNoise(
    area_name="Special Protection Zone",
    max_daytime_limit=50,
    max_night_limit=40,
)
eca_noise2 = EcaNoise(
    area_name="Residential Zone",
    max_daytime_limit=60,
    max_night_limit=50,
)
eca_noise3 = EcaNoise(area_name="Comercial Zone")
eca_noise4 = EcaNoise(area_name="Industry Zone")
db.session.add(eca_noise)
db.session.add(eca_noise2)
db.session.add(eca_noise3)
db.session.add(eca_noise4)
db.session.commit()

qhawax_data1 = {
    "name": "qH004",
    "qhawax_type": "STATIC",
    "state": "ON",
    "availability": "Available",
    "main_aqi": -1.0,
    "mode": "Stand By",
    "on_loop": 0,
    "main_inca": 50.0,
    "first_time_loop": today_midnight,
}
qhawax_data2 = {
    "name": "qH021",
    "qhawax_type": "AEREAL",
    "state": "OFF",
    "availability": "Available2",
    "main_aqi": -1.0,
    "mode": "Customer",
    "on_loop": 0,
    "main_inca": 50.0,
    "first_time_loop": today_midnight,
}
qhawax1 = Qhawax(**qhawax_data1)
qhawax2 = Qhawax(**qhawax_data2)
db.session.add(qhawax1)
db.session.add(qhawax2)
db.session.commit()

qhawax_installation_history_data = {
    "lat": "-7.0000499",
    "lon": "-70.9000000",
    "installation_date_zone": today_midnight,
    "end_date_zone": today_midnight,
    "link_report": "Test",
    "observations": "Test Obs",
    "qhawax_id": qhawax1.id,
    "district": "La Victoria",
    "comercial_name": "Unit Test 1",
    "address": "Test Address",
    "company_id": company.id,
    "eca_noise_id": eca_noise.id,
    "connection_type": "Panel Solar",
    "index_type": "Test Index",
    "season": "Primavera",
    "last_time_physically_turn_on_zone": today_midnight,
    "person_in_charge": "Test Person",
    "is_public": "no",
    "last_registration_time_zone": today_midnight,
}
qhawax_installation_history = QhawaxInstallationHistory(
    **qhawax_installation_history_data
)
db.session.add(qhawax_installation_history)
db.session.commit()

gas_inca_data = {
    "timestamp_zone": today_midnight,
    "qhawax_id": qhawax1.id,
    "main_inca": 50.0,
}
gas_inca = GasInca(**gas_inca_data)
db.session.add(gas_inca)
db.session.commit()

processed_measurement_data = {
    "timestamp": today_midnight,
    "timestamp_zone": today_midnight,
    "qhawax_id": qhawax1.id,
}
processed_measurement = ProcessedMeasurement(**processed_measurement_data)
db.session.add(processed_measurement)
db.session.commit()
