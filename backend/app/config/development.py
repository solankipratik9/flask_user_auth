import os
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Development-specific settings
    SQLALCHEMY_ECHO = True  # Log SQL queries

    # Security (relaxed for development)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # CORS settings for development
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Logging
    LOG_LEVEL = "DEBUG"
