"""Examination API tests."""
from app.core.security import create_access_token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_exam_admin(client, db_session):
    from app.models.user import User
    from app.models.role import Role

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    # enroll role via association table
    from app.models.user_role import UserRole

    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()

    token = create_access_token(data={"sub": str(user.id)})
    resp = client.post(
        "/api/v1/exams",
        json={"code": "DSSSB", "name": "Delhi Subordinate Services Selection Board"},
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["code"] == "DSSSB"


def test_create_exam_student_forbidden(client, db_session):
    from app.models.user import User
    from app.models.role import Role

    student_role = db_session.query(Role).filter(Role.name == "student").first()
    user = User(email="student@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    from app.models.user_role import UserRole

    db_session.add(UserRole(user_id=user.id, role_id=student_role.id))
    db_session.commit()

    token = create_access_token(data={"sub": str(user.id)})
    resp = client.post(
        "/api/v1/exams",
        json={"code": "SSC", "name": "Staff Selection Commission"},
        headers=auth_headers(token),
    )
    assert resp.status_code == 403, resp.text


def test_create_exam_duplicate_code(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin2@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()
    token = create_access_token(data={"sub": str(user.id)})

    client.post(
        "/api/v1/exams",
        json={"code": "UPSC", "name": "Union Public Service Commission"},
        headers=auth_headers(token),
    )
    resp = client.post(
        "/api/v1/exams",
        json={"code": "UPSC", "name": "Duplicate"},
        headers=auth_headers(token),
    )
    assert resp.status_code == 409, resp.text


def test_list_exams(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin3@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()
    token = create_access_token(data={"sub": str(user.id)})

    client.post(
        "/api/v1/exams",
        json={"code": "RRB", "name": "Railway Recruitment Board"},
        headers=auth_headers(token),
    )
    resp = client.get("/api/v1/exams", headers=auth_headers(token))
    assert resp.status_code == 200, resp.text
    codes = {e["code"] for e in resp.json()}
    assert "RRB" in codes
