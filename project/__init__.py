from flask import Flask
from flask_jsglue import JSGlue
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin


# Config
app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app)

# Extensions
db = SQLAlchemy(app)
jsglue = JSGlue(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

from project.main.business import binnacle, company, eca_noise, gas_sensor, qhawax, eca_noise, qhawax_installation_history
from project.main.data import processed_measurement, air_quality,gas_inca, valid_processed_measurement, air_daily_quality
import project.database.models as models
from project.database.models import Company,GasSensor, Qhawax ,ProcessedMeasurement, AirQualityMeasurement, EcaNoise, GasInca, QhawaxInstallationHistory, ValidProcessedMeasurement,AirDailyMeasurement

db.create_all()