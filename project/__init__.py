from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

# Config
app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app,cors_allowed_origins="*",async_handlers=True) 
CORS(app)

# Extensions
db = SQLAlchemy(app)

from project.main.business import company, eca_noise, qhawax, eca_noise, qhawax_installation_history
from project.main.data import processed_measurement, air_quality,gas_inca, drone_flight_log, drone_telemetry
import project.database.models as models
from project.database.models import Company, Qhawax ,ProcessedMeasurement, AirQualityMeasurement, \
									EcaNoise, GasInca, QhawaxInstallationHistory, ValidProcessedMeasurement,\
									DroneTelemetry, DroneFlightLog, TripLog

db.create_all()