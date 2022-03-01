import flask
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


class JSONSupportedToolbar:
    def __init__(self, app):
        @app.after_request
        def after_request(response):
            should_modify_response = (
                response.mimetype == "application/json"
                and flask.request.args.get("debug") == "true"
            )

            if not should_modify_response:
                return response

            html_content = flask.render_template_string(
                "<html><body><pre>{{ response }}</pre></body></html>",
                response=response.data.decode("utf-8"),
            )

            return app.process_response(
                flask.make_response(html_content, response.status_code)
            )

        DebugToolbarExtension(app)


# Config
app = Flask(__name__)
app.config.from_object("config")
socketio = SocketIO(app, cors_allowed_origins="*", async_handlers=True)
CORS(app)

# Extensions
db = SQLAlchemy(app)
if app.debug:
    toolbar = JSONSupportedToolbar(app)

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
