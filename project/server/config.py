import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.getenv('APP_NAME', 'Flask Skeleton')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""


class ProductionConfig(BaseConfig):
    """Production configuration."""
