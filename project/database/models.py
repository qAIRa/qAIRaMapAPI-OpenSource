from project import db


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, unique=True)
    email_group = db.Column(db.String(300), nullable=False, unique=True)
    ruc = db.Column(db.String(11), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    contact_person = db.Column(db.String(100), nullable=False, unique=True)


class Qhawax(db.Model):
    __tablename__ = "qhawax"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, unique=True)
    main_aqi = db.Column(db.Float)
    main_inca = db.Column(db.Float)
    qhawax_type = db.Column(db.String(100), nullable=False, unique=True)
    state = db.Column(db.String(5), nullable=False, unique=True)
    availability = db.Column(db.String(100), nullable=False, unique=True)
    mode = db.Column(db.String(100), nullable=False, unique=True)
    on_loop = db.Column(db.Integer)
    first_time_loop = db.Column(db.DateTime, nullable=False)


class GasInca(db.Model):
    __tablename__ = "gas_inca"
    id = db.Column(db.Integer, primary_key=True)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    CO = db.Column(db.Float)
    CO2 = db.Column(db.Float)
    H2S = db.Column(db.Float)
    NO = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    O3 = db.Column(db.Float)
    PM1 = db.Column(db.Float)
    PM25 = db.Column(db.Float)
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))
    main_inca = db.Column(db.Float)


class EcaNoise(db.Model):
    __tablename__ = "eca_noise"
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100))
    max_daytime_limit = db.Column(db.Integer)
    max_night_limit = db.Column(db.Integer)


class QhawaxInstallationHistory(db.Model):
    __tablename__ = "qhawax_installation_history"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    installation_date_zone = db.Column(db.DateTime, nullable=False)
    end_date_zone = db.Column(db.DateTime, nullable=False)
    link_report = db.Column(db.String(500), nullable=False, unique=True)
    observations = db.Column(db.String(300), nullable=False, unique=True)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))
    district = db.Column(db.String(300), nullable=False, unique=True)
    comercial_name = db.Column(db.String(300), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=False, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    eca_noise_id = db.Column(db.Integer, db.ForeignKey("eca_noise.id"))
    connection_type = db.Column(db.String(300), nullable=False, unique=True)
    index_type = db.Column(db.String(100), nullable=False, unique=True)
    measuring_height = db.Column(db.Integer)
    season = db.Column(db.String(300), nullable=False, unique=True)
    last_time_physically_turn_on_zone = db.Column(db.DateTime, nullable=False)
    person_in_charge = db.Column(db.String(300), nullable=False, unique=True)
    is_public = db.Column(db.String(10), nullable=False, unique=True)
    last_registration_time_zone = db.Column(db.DateTime, nullable=False)
    main_inca = db.Column(db.Float)


class Bitacora(db.Model):
    __tablename__ = "bitacora"
    id = db.Column(db.Integer, primary_key=True)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    observation_type = db.Column(db.String(100))
    description = db.Column(db.String(800))
    solution = db.Column(db.String(800))
    person_in_charge = db.Column(db.String(100))
    start_date_zone = db.Column(db.DateTime, nullable=False)
    end_date_zone = db.Column(db.DateTime, nullable=False)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))


class AirQualityMeasurement(db.Model):
    __tablename__ = "air_quality_measurement"
    id = db.Column(db.Integer, primary_key=True)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    CO = db.Column(db.Float)
    CO_ug_m3 = db.Column(db.Float)
    H2S = db.Column(db.Float)
    H2S_ug_m3 = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    NO2_ug_m3 = db.Column(db.Float)
    O3 = db.Column(db.Float)
    O3_ug_m3 = db.Column(db.Float)
    PM25 = db.Column(db.Float)
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    SO2_ug_m3 = db.Column(db.Float)
    uv = db.Column(db.Float)
    uva = db.Column(db.Float)
    uvb = db.Column(db.Float)
    spl = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    alt = db.Column(db.Float)
    I_temperature = db.Column(db.Float)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))


class ProcessedMeasurement(db.Model):
    __tablename__ = "processed_measurement"
    id = db.Column(db.Integer, primary_key=True)
    CO = db.Column(db.Float)
    CO_ug_m3 = db.Column(db.Float)
    CO2 = db.Column(db.Float)
    H2S = db.Column(db.Float)
    H2S_ug_m3 = db.Column(db.Float)
    NO = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    NO2_ug_m3 = db.Column(db.Float)
    O3 = db.Column(db.Float)
    O3_ug_m3 = db.Column(db.Float)
    PM1 = db.Column(db.Float)
    PM25 = db.Column(db.Float)
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    SO2_ug_m3 = db.Column(db.Float)
    VOC = db.Column(db.Float)
    UV = db.Column(db.Float)
    UVA = db.Column(db.Float)
    UVB = db.Column(db.Float)
    spl = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    alt = db.Column(db.Float)
    I_temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, nullable=False)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))


class ValidProcessedMeasurement(db.Model):
    __tablename__ = "valid_processed_measurement"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    CO = db.Column(db.Float)
    CO_ug_m3 = db.Column(db.Float)
    CO2 = db.Column(db.Float)
    H2S = db.Column(db.Float)
    H2S_ug_m3 = db.Column(db.Float)
    NO = db.Column(db.Float)
    NO2 = db.Column(db.Float)
    NO2_ug_m3 = db.Column(db.Float)
    O3 = db.Column(db.Float)
    O3_ug_m3 = db.Column(db.Float)
    PM1 = db.Column(db.Float)
    PM25 = db.Column(db.Float)
    PM10 = db.Column(db.Float)
    SO2 = db.Column(db.Float)
    SO2_ug_m3 = db.Column(db.Float)
    VOC = db.Column(db.Float)
    UV = db.Column(db.Float)
    UVA = db.Column(db.Float)
    UVB = db.Column(db.Float)
    SPL = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    alt = db.Column(db.Float)
    I_temperature = db.Column(db.Float)
    qhawax_installation_id = db.Column(
        db.Integer, db.ForeignKey("qhawax_installation_history.id")
    )


class DroneTelemetry(db.Model):
    __tablename__ = "drone_telemetry"

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    airspeed = db.Column(db.Float(precision=2))
    alt = db.Column(db.Float(precision=2))
    battery_perc = db.Column(db.Float(precision=2))
    dist_home = db.Column(db.Float(precision=2))
    compass1_x = db.Column(db.Integer)
    compass1_y = db.Column(db.Integer)
    compass1_z = db.Column(db.Integer)
    compass2_x = db.Column(db.Integer)
    compass2_y = db.Column(db.Integer)
    compass2_z = db.Column(db.Integer)
    compass_variance = db.Column(db.Float(precision=2))
    current = db.Column(db.Float(precision=2))
    fix_type = db.Column(db.Integer)
    flight_mode = db.Column(db.String(300))
    gps_sats = db.Column(db.Integer)
    gps_fix = db.Column(db.Integer)
    gps2_sats = db.Column(db.Integer)
    gps2_fix = db.Column(db.Integer)
    irlock_x = db.Column(db.Float(precision=2))
    irlock_y = db.Column(db.Float(precision=2))
    irlock_status = db.Column(db.Boolean)
    lat = db.Column(db.Float(precision=8))
    lon = db.Column(db.Float(precision=8))
    num_gps = db.Column(db.Integer)
    pos_horiz_variance = db.Column(db.Float(precision=2))
    pos_vert_variance = db.Column(db.Float(precision=2))
    rcout1 = db.Column(db.Integer)
    rcout2 = db.Column(db.Integer)
    rcout3 = db.Column(db.Integer)
    rcout4 = db.Column(db.Integer)
    rcout5 = db.Column(db.Integer)
    rcout6 = db.Column(db.Integer)
    rcout7 = db.Column(db.Integer)
    rcout8 = db.Column(db.Integer)
    sonar_dist = db.Column(db.Float(precision=2))
    throttle = db.Column(db.Integer)
    vibrations_x = db.Column(db.Float(precision=10))
    vibrations_y = db.Column(db.Float(precision=10))
    vibrations_z = db.Column(db.Float(precision=10))
    voltage = db.Column(db.Float(precision=2))
    velocity_variance = db.Column(db.Float(precision=2))
    terrain_alt_variance = db.Column(db.Float(precision=2))
    waypoint = db.Column(db.Integer)
    yaw = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))


class DroneFlightLog(db.Model):
    __tablename__ = "drone_flight_log"
    id = db.Column(db.Integer, primary_key=True)
    flight_start = db.Column(db.DateTime, nullable=False)
    flight_end = db.Column(db.DateTime, nullable=False)
    flight_detail = db.Column(db.String(100))
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))


class TripLog(db.Model):
    __tablename__ = "trip_log"
    id = db.Column(db.Integer, primary_key=True)
    trip_start = db.Column(db.DateTime, nullable=False)
    trip_end = db.Column(db.DateTime)
    details = db.Column(db.String(100))
    qhawax_id = db.Column(db.Integer, db.ForeignKey("qhawax.id"))
