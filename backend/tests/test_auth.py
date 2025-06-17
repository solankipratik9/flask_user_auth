import pytest
from app.extensions import redis_client
from app.services.user_service import UserService
from flask_jwt_extended import create_access_token, get_jti



def test_register_user(client):
    res = client.post(
        "/auth/register",
        json={
            "email": "test_user1@local.com",
            "password": "Secure12345",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert res.status_code == 201
    assert "access_token" in res.json


def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "email": "test_user2@local.com",
            "password": "Secure12345",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    res = client.post(
        "/auth/login", json={"email": "test_user2@local.com", "password": "Secure12345"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"email": "wrongpass@local.com", "password": "Correctpass1"},
    )
    res = client.post(
        "/auth/login", json={"email": "wrongpass@local.com", "password": "wrongpass"}
    )
    assert res.status_code == 401


def test_login_unregistered_user(client):
    res = client.post(
        "/auth/login", json={"email": "unknown@local.com", "password": "any"}
    )
    assert res.status_code == 401


def test_refresh_token(client):
    login_res = client.post(
        "/auth/register",
        json={"email": "test_user3@local.com", "password": "Secure12345"},
    )
    refresh_token = login_res.json.get("refresh_token")
    res = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json


def test_refresh_token_missing(client):
    res = client.post("/auth/refresh")
    assert res.status_code == 401


def test_logout_token_revoked(client, app):
    with app.app_context():
        user = UserService.create_user(
            email="user_logout@local.com",
            password="UserLogout123",
            first_name="User",
            last_name="Logout",
        )
        token = create_access_token(identity=user.id)
        jti = get_jti(token)

    # No mocking needed - FakeRedis works like real Redis
    res = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

    # Check if token was blacklisted
    assert redis_client.get(jti) == "revoked"


def test_get_current_user(client):
    login_res = client.post(
        "/auth/register",
        json={"email": "test_user4@local.com", "password": "Secure12345"},
    )
    access_token = login_res.json.get("access_token")
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert res.json["email"] == "test_user4@local.com"


def test_get_current_user_no_token(client):
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_health_check(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json.get("status") == "healthy"


def test_get_users(client):
    client.post(
        "/auth/register",
        json={
            "email": "user1@local.com",
            "password": "User123456",
            "first_name": "User",
            "last_name": "One",
        },
    )
    client.post(
        "/auth/register",
        json={
            "email": "user2@local.com",
            "password": "User234567",
            "first_name": "User",
            "last_name": "Two",
        },
    )
    login_res = client.post(
        "/auth/login", json={"email": "user1@local.com", "password": "User123456"}
    )
    token = login_res.json["access_token"]
    res = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    users = res.json["users"]
    assert res.status_code == 200
    assert isinstance(users, list)


def test_get_users_unauthorized(client):
    res = client.get("/api/v1/users")
    assert res.status_code == 401


def test_get_user_by_id(client):
    register = client.post(
        "/auth/register",
        json={
            "email": "test_id@local.com",
            "password": "Test123456",
            "first_name": "Test",
            "last_name": "ID",
        },
    )
    token = register.json["access_token"]

    user_list = client.get(
        "/api/v1/users", headers={"Authorization": f"Bearer {token}"}
    )
    users = user_list.json["users"]
    for user in users:
        if user["email"] == "test_id@local.com":
            user_id = user["id"]
            break
    else:
        pytest.fail("User not found in the list")

    res = client.get(
        f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json["email"] == "test_id@local.com"


def test_get_user_by_id_unauthorized(client):
    res = client.get("/api/v1/users/1")
    assert res.status_code in [401, 422]


def test_get_user_not_found(client):
    client.post(
        "/auth/register",
        json={
            "email": "lookup@local.com",
            "password": "Pass123456",
            "first_name": "Lookup",
            "last_name": "User",
        },
    )
    login = client.post(
        "/auth/login", json={"email": "lookup@local.com", "password": "Pass123456"}
    )
    token = login.json["access_token"]
    res = client.get(
        "/api/v1/users/99999", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
