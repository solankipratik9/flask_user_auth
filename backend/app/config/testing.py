from datetime import timedelta
from .base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    REDIS_URL = None
    SECRET_KEY="7ERLB5EWzNq1BbU1q4qnaZw8We9TciMGvt3qJig9DPc5Fk2xgqPKFzmcUBFFKq"
    JWT_SECRET_KEY="8Wea7NzhUHbAMcfMGEVvu53A4zFxVFm7DThGEuXSgpQCFKZj05Yd6LYXF2ZWUY"

    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Faster password hashing for tests
    BCRYPT_LOG_ROUNDS = 4

    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False

    # JWT settings for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
