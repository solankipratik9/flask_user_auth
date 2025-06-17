from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from uuid import UUID


class UserService:
    @staticmethod
    def create_user(email, password, **kwargs):
        try:
            user = User(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=kwargs.get("first_name", ""),
                last_name=kwargs.get("last_name", ""),
            )
            return user.save()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User with this email already exists")

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email, is_active=True).first()

    @staticmethod
    def get_user_by_id(user_id):
        try:
            if isinstance(user_id, str):
                user_id = UUID(user_id)
            return User.query.filter_by(id=user_id, is_active=True).first()
        except ValueError:
            return None

    @staticmethod
    def get_users_paginated(page=1, per_page=20):
        return User.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        for key, value in kwargs.items():
            if hasattr(user, key) and key != "password_hash":
                setattr(user, key, value)

        return user.save()

    @staticmethod
    def deactivate_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        return user.delete()
