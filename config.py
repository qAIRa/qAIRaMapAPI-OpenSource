import os
basedir = os.path.abspath(os.path.dirname(__file__))
# You need to replace the next values with the appropriate values for your configuration

env = 'local'
if env == 'local':
    print('Using release configuration...')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_KEY = os.environ.get('TOKEN_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_RECEIVER = 'l.montalvo@qairadrones.com'
    BASE_URL = 'http://0.0.0.0:5000/'
elif env == 'dev':
    print('Using release configuration...')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_KEY = os.environ.get('TOKEN_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_RECEIVER = os.environ.get('MAIL_DEFAULT_RECEIVER')
    BASE_URL = 'https://qairamapnapi-dev.qairadrones.com/'
elif env == 'prod':
    print('Using release configuration...')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_KEY = os.environ.get('TOKEN_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_RECEIVER = os.environ.get('MAIL_DEFAULT_RECEIVER')
    BASE_URL = 'https://qairamapnapi.qairadrones.com/'

# Gmail authentication
ADMIN_EMAIL = os.environ.get('MAIL_USERNAME')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
MAIL_SENDER = os.environ.get('MAIL_USERNAME')
# Mail settings
MAIL_SERVER_PORT = 'smtp.googlemail.com:587'