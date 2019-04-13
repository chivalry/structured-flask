import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Base configuration."""

    ADMINS = ['chivalry@mac.com']
    APP_NAME = os.getenv('APP_NAME', 'Flask Skeleton')
    BCRYPT_LOG_ROUNDS = 4
    DEBUG_TB_ENABLED = False
    LANGUAGES = ['en']
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    """Development configuration."""

    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'dev.db'))


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'sqlite://')


class ProdConfig(Config):
    """Production configuration."""

    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
