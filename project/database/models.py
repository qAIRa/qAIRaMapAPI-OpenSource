from project import db

class Company(db.Model):
    __tablename__ = 'company'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, unique=True)
    email_group = db.Column(db.String(300), nullable=False, unique=True)
    ruc = db.Column(db.String(11), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    contact_person = db.Column(db.String(100), nullable=False, unique=True)
    installations = db.relationship('QhawaxInstallationHistory', backref='company', lazy='subquery',
                             cascade='delete, delete-orphan')
class Qhawax(db.Model):
    __tablename__ = 'qhawax'
    
    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False, unique=True)
    main_aqi = db.Column(db.Float)
    main_inca = db.Column(db.Float)
    qhawax_type = db.Column(db.String(100), nullable=False, unique=True)
    state = db.Column(db.String(5), nullable=False, unique=True)
    availability = db.Column(db.String(100), nullable=False, unique=True)
    mode = db.Column(db.String(100), nullable=False, unique=True)
    firmware_version_id = db.Column(db.Integer, db.ForeignKey('firmware_version.id'))
    last_firmware_update = db.Column(db.DateTime, nullable=False)
    on_loop = db.Column(db.Integer)
    first_time_loop = db.Column(db.DateTime, nullable=False)

class GasSensor(db.Model):
    __tablename__ = 'gas_sensor'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), nullable=False, unique=True)
    purchase_date = db.Column(db.DateTime)
    type = db.Column(db.String(100))
    WE = db.Column(db.Float)
    AE = db.Column(db.Float)
    sensitivity = db.Column(db.Float)
    sensitivity_2 = db.Column(db.Float)
    C2 = db.Column(db.Float, nullable=False, default=0, server_default='0')
    C1 = db.Column(db.Float, nullable=False, default=1, server_default='1')
    C0 = db.Column(db.Float, nullable=False, default=0, server_default='0')
    NC1 = db.Column(db.Float, nullable=False, default=1, server_default='1')
    NC0 = db.Column(db.Float, nullable=False, default=0, server_default='0')
    A_OPC = db.Column(db.Float, nullable=False, default=1, server_default='1')
    B_OPC = db.Column(db.Float, nullable=False, default=0, server_default='0')
    algorithm = db.Column(db.Integer)
    WEt = db.Column(db.Float)
    AEt = db.Column(db.Float)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))

class GasInca(db.Model):
    __tablename__ = 'gas_inca'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
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
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))
    main_inca = db.Column(db.Float)
    
class EcaNoise(db.Model):
    __tablename__ = 'eca_noise'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100))
    max_daytime_limit = db.Column(db.Integer)
    max_night_limit = db.Column(db.Integer)
    installations = db.relationship('QhawaxInstallationHistory',
                                    backref='eca_noise', lazy='subquery', cascade='delete, delete-orphan') 

class QhawaxInstallationHistory(db.Model):
    __tablename__ = 'qhawax_installation_history'

        # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    installation_date_zone = db.Column(db.DateTime, nullable=False)
    end_date_zone = db.Column(db.DateTime, nullable=False)
    link_report = db.Column(db.String(500), nullable=False, unique=True)
    observations = db.Column(db.String(300), nullable=False, unique=True)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))
    district = db.Column(db.String(300), nullable=False, unique=True)
    comercial_name = db.Column(db.String(300), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=False, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    eca_noise_id = db.Column(db.Integer, db.ForeignKey('eca_noise.id'))
    connection_type = db.Column(db.String(300), nullable=False, unique=True)
    index_type = db.Column(db.String(100), nullable=False, unique=True)
    measuring_height = db.Column(db.Integer)
    season = db.Column(db.String(300), nullable=False, unique=True)
    last_time_physically_turn_on_zone = db.Column(db.DateTime, nullable=False)
    person_in_charge = db.Column(db.String(300), nullable=False, unique=True)
    is_public  = db.Column(db.String(10), nullable=False, unique=True)
    last_registration_time_zone = db.Column(db.DateTime, nullable=False)
    main_inca = db.Column(db.Float) 
    last_cleaning_equipment_date = db.Column(db.DateTime, nullable=False)
    last_cleaning_area_date = db.Column(db.DateTime, nullable=False)
    last_maintenance_date = db.Column(db.DateTime, nullable=False)

class Bitacora(db.Model):
    __tablename__ = 'bitacora'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    timestamp_zone = db.Column(db.DateTime, nullable=False)
    observation_type = db.Column(db.String(100))
    description = db.Column(db.String(800))
    solution = db.Column(db.String(800))
    person_in_charge = db.Column(db.String(100))
    start_date_zone = db.Column(db.DateTime, nullable=False)
    end_date_zone = db.Column(db.DateTime, nullable=False)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))

class AirDailyMeasurement(db.Model):
    __tablename__ = 'air_daily_measurement'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
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
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    UV = db.Column(db.Float)
    spl = db.Column(db.Float)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))

class AirQualityMeasurement(db.Model):
    __tablename__ = 'air_quality_measurement'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
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
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))

class ProcessedMeasurement(db.Model):
    __tablename__ = 'processed_measurement'

    # Column's definition
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
    spl = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    alt = db.Column(db.Float)
    I_temperature = db.Column(db.Float)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))


class ValidProcessedMeasurement(db.Model):
    __tablename__ = 'valid_processed_measurement'

    # Column's definition
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
    qhawax_installation_id = db.Column(db.Integer, db.ForeignKey('qhawax_installation_history.id'))

class FirmwareUpdate(db.Model):
    __tablename__ = 'firmware_update'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    qhawax_id = db.Column(db.Integer, db.ForeignKey('qhawax.id'))
    date_of_update = db.Column(db.DateTime, nullable=False)
    url_of_bif_file = db.Column(db.String(1000), nullable=False, unique=True)
    number_of_frames = db.Column(db.Integer)
    number_of_bytes = db.Column(db.Integer)
    firmware_version_id = db.Column(db.Integer, db.ForeignKey('firmware_version.id'))
    frames = db.relationship('Frame', backref='firmware_update', lazy='subquery',
                                                cascade='delete, delete-orphan')

class Frame(db.Model):
    __tablename__ = 'frame'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    firmware_update_id = db.Column(db.Integer, db.ForeignKey('firmware_update.id'))
    numbering_by_frame = db.Column(db.Integer)
    data_lenght = db.Column(db.Integer)
    data = db.Column(db.String(1000), nullable=False, unique=True)
    crc1 = db.Column(db.Integer)
    crc2 = db.Column(db.Integer)
    crc3 = db.Column(db.Integer)
    crc4 = db.Column(db.Integer)

class FirmwareVersion(db.Model):
    __tablename__ = 'firmware_version'

    # Column's definition
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(250))
    qhawax_type = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, nullable=False)
    qhawaxs = db.relationship('Qhawax', backref='firmware_version', lazy='subquery',
                                                cascade='delete, delete-orphan')
    firmware_updates = db.relationship('FirmwareUpdate', backref='firmware_version', lazy='subquery',
                                                cascade='delete, delete-orphan')

import project.database.utils as utils