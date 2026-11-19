"""Authentication API tests."""
from app.schemas.user import UserCreate


def test_register_success(client):
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "Secret1234", "display_alias": "alice"},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert data["display_alias"] == "alice"
    assert "id" in data


def test_register_duplicate_email(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "Secret1234"},
    )
    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "Secret1234"},
    )
    assert resp.status_code == 409, resp.text


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "carol@example.com", "password": "Secret1234"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        params={"email": "carol@example.com", "password": "Secret1234"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    resp = client.post(
        "/api/v1/auth/login",
        params={"email": "none@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_refresh_issues_new_tokens(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "dave@example.com", "password": "Secret1234"},
    )
    login = client.post(
        "/api/v1/auth/login",
        params={"email": "dave@example.com", "password": "Secret1234"},
    )
    refresh_token = login.json()["refresh_token"]
    resp = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert resp.status_code == 200, resp.text
    assert "access_token" in resp.json()
