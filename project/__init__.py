from flask import Flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Config
app = Flask(__name__)
app.config.from_object("config")
socketio = SocketIO(app, cors_allowed_origins="*", async_handlers=True)
CORS(app)

# Extensions
db = SQLAlchemy(app)

import project.database.models as models
from project.database.models import (AirQualityMeasurement, Company,
                                     DroneFlightLog, DroneTelemetry, EcaNoise,
                                     GasInca, ProcessedMeasurement, Qhawax,
                                     QhawaxInstallationHistory, TripLog,
                                     ValidProcessedMeasurement)
from project.main.business import (company, eca_noise, qhawax,
                                   qhawax_installation_history)
from project.main.data import (air_quality, drone_flight_log, drone_telemetry,
                               gas_inca, processed_measurement)

db.create_all()
