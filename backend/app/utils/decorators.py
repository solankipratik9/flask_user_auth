from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService


def admin_required(f):
    """Decorator to require admin privileges."""

    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_id(current_user_id)

        if not user or not getattr(user, "is_admin", False):
            return {"error": "Admin privileges required"}, 403

        return f(*args, **kwargs)

    return decorated_function


def validate_json(required_fields=None):
    """Decorator to validate JSON request data."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return {"error": "Content-Type must be application/json"}, 400

            data = request.get_json()
            if not data:
                return {"error": "No JSON data provided"}, 400

            if required_fields:
                missing_fields = [
                    field for field in required_fields if field not in data
                ]
                if missing_fields:
                    return {
                        "error": f'Missing required fields: {", ".join(missing_fields)}'
                    }, 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator
