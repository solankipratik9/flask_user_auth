import os
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # CORS settings for production
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "/var/log/flask-app.log"
