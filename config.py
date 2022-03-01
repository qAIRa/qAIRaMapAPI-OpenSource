import os

basedir = os.path.abspath(os.path.dirname(__file__))
# You need to replace the next values with the appropriate values for your configuration

env = "prod"
if env == "local":
    print("Using local configuration...")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_OPEN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = "http://0.0.0.0:5000/"
    DEBUG = True
    SECRET_KEY = "my-secret-key"
elif env == "prod":
    print("Using release configuration...")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI_OPEN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = "https://openqairamapnapi.qairadrones.com/"
    DEBUG = False
    SECRET_KEY = "my-secret-key"  # TODO: Replace with a more secure key, and don't push it to Github
