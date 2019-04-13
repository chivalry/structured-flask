import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Base configuration."""

    APP_NAME = os.getenv('APP_NAME', 'Flask Skeleton')
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-secret')
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    WTF_CSRF_ENABLED = False
    ADMINS = ['chivalry@mac.com']
    LANGUAGES = ['en']


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

    WTF_CSRF_ENABLED = True
