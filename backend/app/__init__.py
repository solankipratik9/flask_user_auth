from flask import Flask
from app.extensions import db, migrate, jwt, cors, limiter
from app.config import get_config


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500


def create_app(config_name=None):
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.v1 import api_v1_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    # Error handlers
    register_error_handlers(app)

    return app
