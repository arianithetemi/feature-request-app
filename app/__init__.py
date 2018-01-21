from flask import Flask
import os, pymysql
import ConfigParser
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# SQLAlchemy
db = SQLAlchemy();

# Initialize bcrypt
bcrypt = Bcrypt()

# Generating random 24 chars for secret key
secret_key = os.urandom(24).encode('hex')

def create_app():
    # Here we  create flask instance
    app = Flask(__name__)

    # Allow cross-domain access to API.
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize bcrypt
    bcrypt.init_app(app)

    # Init modules
    init_modules(app)

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    # Testing app config path
    testapp_config_filepath = app_dir + '/test_app_config.cfg'

    # Checking if config.cfg file exists and read from it, if not read from test config
    if os.path.isfile(config_filepath):
        config.read(config_filepath)
        # Getting DB Config
        username = config.get('SQLAlchemy', 'SQL_USERNAME')
        password = config.get('SQLAlchemy', 'SQL_PASSWORD')
        server = config.get('SQLAlchemy', 'SQL_HOST')
        db_name = config.get('SQLAlchemy', 'SQL_DB_NAME')
        sqlalchemy_db_uri = 'mysql+pymysql://' + username + ':' + password + '@' + server + '/' + db_name
    else:
        config.read(testapp_config_filepath)
        sqlalchemy_db_uri = config.get('SQLAlchemy', 'SQLALCHEMY_DATABASE_URI')

    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24).encode('hex')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()

def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to.
    # Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)


def init_modules(app):

    # Import blueprint modules
    from app.mod_main.views import mod_main
    from app.mod_user_api.views import mod_user_api
    from app.mod_auth_api.views import mod_auth_api

    app.register_blueprint(mod_main)
    app.register_blueprint(mod_user_api)
    app.register_blueprint(mod_auth_api)
