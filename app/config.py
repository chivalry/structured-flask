import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Base configuration."""

    ADMINS = ['chivalry@mac.com']
    APP_NAME = os.getenv('APP_NAME', 'Structured Flask')
    BCRYPT_LOG_ROUNDS = 4
    DEBUG_TB_ENABLED = False
    DEBUG_TB_PROFILER_ENABLED = True
    LANGUAGES = ['en']
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-secret')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = os.getenv('MAIL_PORT', 25)
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'admin@example.com')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    """Development configuration."""

    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    db_path = os.path.join(basedir, 'dev.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'


class TestConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'sqlite://')


class ProdConfig(Config):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
