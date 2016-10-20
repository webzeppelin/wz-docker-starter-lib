"""This module has configurations for flask app."""

import os
import logging
from logging import handlers
from flask import Flask
from flask_cors import CORS
from .utils.encode import MyFlaskJSONEncoder

app = Flask(__name__)

HOSTNAME = '0.0.0.0'
PORT = 8081
REDIS_HOST = 'redis'
REDIS_PORT = 6379

CONFIG = {
    "development": "flask_app.config.DevelopmentConfig",
    "testing": "flask_app.config.TestingConfig",
    "production": "flask_app.config.ProductionConfig",
    "default": "flask_app.config.ProductionConfig"
}


class BaseConfig(object):
    """Base class for default set of configs."""

    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = "[%(asctime)s] [%(funcName)-30s] +\
                                    [%(levelname)-6s] %(message)s"
    LOGGING_LOCATION = 'web.log'
    LOGGING_LEVEL = logging.DEBUG
    CACHE_TYPE = 'simple'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']

    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class DevelopmentConfig(BaseConfig):
    """Default set of configurations for development mode."""

    DEBUG = True
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(BaseConfig):
    """Default set of configurations for prod mode."""

    DEBUG = False
    TESTING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))


class TestingConfig(BaseConfig):
    """Default set of configurations for test mode."""

    DEBUG = False
    TESTING = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

def setup_logger():
    """Setup the logger with predefined formatting of time and rollup."""
    generated_files = 'log_output'
    logfile_name = '{0}/web.log'.format(generated_files)
    if not os.path.exists(generated_files):
        os.makedirs(generated_files)

    logging.getLogger('').setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(logfile_name,
                                                   maxBytes=10000000,
                                                   backupCount=1000)
    LOGGING_FORMAT = "[%(asctime)s] [%(name)s.%(funcName)-30s]" +\
        "[%(levelname)-6s] %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT, datefmt=datefmt))
    logging.getLogger('').addHandler(handler)

    print('Logging into {}'.format(logfile_name))


def configure_app(app):
    """Configure the app w.r.t Flask-security, databases, loggers."""
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(CONFIG[config_name])

    setup_logger()
    
    # set up cross origin handling
    CORS(app, headers=['Content-Type'])

    app.json_encoder = MyFlaskJSONEncoder
    app.redis_config = RedisConfig()

class RedisConfig(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.hostname = host
        self.port = port
