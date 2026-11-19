"""Syllabus version API tests."""
from app.core.security import create_access_token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _make_admin(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin_syllabus@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()
    return user


def test_create_syllabus_version(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "SYLL_TEST", "name": "Syllabus Test Exam"},
        headers=auth_headers(token),
    ).json()

    resp = client.post(
        "/api/v1/syllabus-versions",
        json={
            "exam_id": exam["id"],
            "version": "2.0",
            "title": "Updated Syllabus",
            "description": "Revised syllabus for 2025",
            "effective_from": "2025-01-01",
            "is_active": True,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["version"] == "2.0"
    assert data["title"] == "Updated Syllabus"
    assert data["is_active"] is True


def test_list_syllabus_versions_by_exam(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "SYLL_LIST", "name": "Syllabus List Exam"},
        headers=auth_headers(token),
    ).json()

    client.post(
        "/api/v1/syllabus-versions",
        json={
            "exam_id": exam["id"],
            "version": "1.0",
            "title": "Syllabus v1",
            "is_active": False,
        },
        headers=auth_headers(token),
    )
    client.post(
        "/api/v1/syllabus-versions",
        json={
            "exam_id": exam["id"],
            "version": "2.0",
            "title": "Syllabus v2",
            "is_active": True,
        },
        headers=auth_headers(token),
    )

    resp = client.get(
        f"/api/v1/syllabus-versions?exam_id={exam['id']}",
        headers=auth_headers(token),
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) == 2


def test_update_syllabus_version(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "SYLL_UPD", "name": "Syllabus Update Exam"},
        headers=auth_headers(token),
    ).json()

    created = client.post(
        "/api/v1/syllabus-versions",
        json={
            "exam_id": exam["id"],
            "version": "1.0",
            "title": "Original Title",
            "is_active": True,
        },
        headers=auth_headers(token),
    ).json()

    resp = client.patch(
        f"/api/v1/syllabus-versions/{created['id']}",
        json={
            "exam_id": exam["id"],
            "version": "1.1",
            "title": "Updated Title",
            "is_active": True,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["version"] == "1.1"
    assert data["title"] == "Updated Title"


def test_create_syllabus_version_student_forbidden(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    # Create admin and exam first
    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    admin = User(email="admin_for_syllabus@example.com", password_hash="x")
    db_session.add(admin)
    db_session.commit()
    db_session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
    db_session.commit()
    admin_token = create_access_token(data={"sub": str(admin.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "STU_SYLL_EXAM", "name": "Student Syllabus Exam"},
        headers=auth_headers(admin_token),
    ).json()

    # Now try as student
    student_role = db_session.query(Role).filter(Role.name == "student").first()
    user = User(email="student_syllabus@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=student_role.id))
    db_session.commit()
    token = create_access_token(data={"sub": str(user.id)})

    resp = client.post(
        "/api/v1/syllabus-versions",
        json={
            "exam_id": exam["id"],
            "version": "1.0",
            "title": "Student Syllabus",
            "is_active": True,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 403, resp.text
