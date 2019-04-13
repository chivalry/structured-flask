import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv('APP_NAME', 'Flask Skeleton')
    SECRET_KEY = os.getenv('SECRET_KEY', 'not-secret')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""


class ProductionConfig(BaseConfig):
    """Production configuration."""
