import os
from app.settings import PG_DB

from settings import PG_HOST, PG_USER, PG_PASS


class Config(object):
    """
    Configuration base, for all environments.
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///application.db"
    )
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"postgresql://${PG_USER}:{PG_PASS}@{PG_HOST}/{PG_DB}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
