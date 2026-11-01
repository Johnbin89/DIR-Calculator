import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

dotenv_file = os.path.join(basedir, '.env')
if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # Comma-separated. Needed behind Traefik: it marks WebSocket upgrades as wss, so
    # Socket.IO's default same-origin check rejects the browser's https:// origin.
    SOCKETIO_ALLOWED_ORIGINS = os.environ['SOCKETIO_ALLOWED_ORIGINS'].split(',') \
        if os.environ.get('SOCKETIO_ALLOWED_ORIGINS') else None

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}