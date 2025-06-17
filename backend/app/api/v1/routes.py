from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import api_v1_bp
from app.services.user_service import UserService
from app.extensions import limiter


@api_v1_bp.route("/users", methods=["GET"])
@jwt_required()
@limiter.limit("100 per hour")
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    users_pagination = UserService.get_users_paginated(page=page, per_page=per_page)

    return {
        "users": [
            {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "created_at": user.created_at.isoformat(),
            }
            for user in users_pagination.items
        ],
        "pagination": {
            "page": users_pagination.page,
            "pages": users_pagination.pages,
            "per_page": users_pagination.per_page,
            "total": users_pagination.total,
            "has_next": users_pagination.has_next,
            "has_prev": users_pagination.has_prev,
        },
    }


@api_v1_bp.route("/users/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


@api_v1_bp.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy", "service": "flask-api"}

@api_v1_bp.route("/test-celery", methods=["GET"])
def test_celery():
    from app.celery_app import send_email_task

    result = send_email_task.delay("you@example.com", "Test Celery", "This is a test email.")
    return {"task_id": result.id, "status": "Task dispatched"}
