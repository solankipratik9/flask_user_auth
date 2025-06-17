from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import check_password_hash
from app.api.auth import auth_bp
from app.services.user_service import UserService
from app.utils.validators import validate_email, validate_password
from app.extensions import limiter, redis_client


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json()

    # Validation
    if not data or not data.get("email") or not data.get("password"):
        return {"error": "Email and password are required"}, 400

    if not validate_email(data["email"]):
        return {"error": "Invalid email format"}, 400

    if not validate_password(data["password"]):
        return {"error": "Password must be at least 8 characters"}, 400

    try:
        user = UserService.create_user(
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "message": "User created successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }, 201

    except ValueError as e:
        return {"error": str(e)}, 400


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return {"error": "Email and password are required"}, 400

    user = UserService.get_user_by_email(data["email"])

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    redis_client.set(jti, "revoked", ex=3600)
    return jsonify(msg="Successfully logged out"), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    return {"access_token": new_token}


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at.isoformat(),
    }
