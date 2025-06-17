import os
import redis
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery

# Database
db = SQLAlchemy()
migrate = Migrate()

# Authentication
jwt = JWTManager()

# Blocklist check
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis_client.get(jti) is not None

# CORS
cors = CORS()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URL"),
    default_limits=["1000 per hour"])


# Redis
def get_redis_client():
    redis_url = os.environ.get("REDIS_URL")

    if redis_url and not os.environ.get("TESTING"):
        return redis.Redis.from_url(redis_url, decode_responses=True)
    else:
        # Use FakeRedis for testing and development
        from fakeredis import FakeRedis
        return FakeRedis(decode_responses=True)


redis_client = get_redis_client()


# Celery (for background tasks)
celery = Celery()
