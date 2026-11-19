"""Exam-subject mapping API tests."""
from app.core.security import create_access_token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _make_admin(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin_mapping@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()
    return user


def test_create_exam_subject_mapping(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "MAP_TEST", "name": "Mapping Test Exam"},
        headers=auth_headers(token),
    ).json()

    subject = client.post(
        "/api/v1/subjects",
        json={"code": "MATH", "name": "Mathematics"},
        headers=auth_headers(token),
    ).json()

    resp = client.post(
        "/api/v1/exam-subjects",
        json={
            "exam_id": exam["id"],
            "subject_id": subject["id"],
            "weightage": 25.0,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["weightage"] == 25.0
    assert data["exam_id"] == exam["id"]
    assert data["subject_id"] == subject["id"]


def test_duplicate_mapping_conflict(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "DUP_MAP", "name": "Duplicate Map Exam"},
        headers=auth_headers(token),
    ).json()

    subject = client.post(
        "/api/v1/subjects",
        json={"code": "SCI", "name": "Science"},
        headers=auth_headers(token),
    ).json()

    client.post(
        "/api/v1/exam-subjects",
        json={
            "exam_id": exam["id"],
            "subject_id": subject["id"],
            "weightage": 30.0,
        },
        headers=auth_headers(token),
    )

    resp = client.post(
        "/api/v1/exam-subjects",
        json={
            "exam_id": exam["id"],
            "subject_id": subject["id"],
            "weightage": 40.0,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 409, resp.text


def test_list_mappings_by_exam(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "LIST_MAP", "name": "List Map Exam"},
        headers=auth_headers(token),
    ).json()

    subject1 = client.post(
        "/api/v1/subjects",
        json={"code": "ENG", "name": "English"},
        headers=auth_headers(token),
    ).json()
    subject2 = client.post(
        "/api/v1/subjects",
        json={"code": "HIN", "name": "Hindi"},
        headers=auth_headers(token),
    ).json()

    client.post(
        "/api/v1/exam-subjects",
        json={"exam_id": exam["id"], "subject_id": subject1["id"], "weightage": 40.0},
        headers=auth_headers(token),
    )
    client.post(
        "/api/v1/exam-subjects",
        json={"exam_id": exam["id"], "subject_id": subject2["id"], "weightage": 60.0},
        headers=auth_headers(token),
    )

    resp = client.get(
        f"/api/v1/exam-subjects?exam_id={exam['id']}",
        headers=auth_headers(token),
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) == 2


def test_create_exam_subject_student_forbidden(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    # Create admin and exam/subject first
    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    admin = User(email="admin_for_map@example.com", password_hash="x")
    db_session.add(admin)
    db_session.commit()
    db_session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
    db_session.commit()
    admin_token = create_access_token(data={"sub": str(admin.id)})

    exam = client.post(
        "/api/v1/exams",
        json={"code": "STU_MAP_EXAM", "name": "Student Map Exam"},
        headers=auth_headers(admin_token),
    ).json()
    subject = client.post(
        "/api/v1/subjects",
        json={"code": "GEO", "name": "Geography"},
        headers=auth_headers(admin_token),
    ).json()

    # Now try as student
    student_role = db_session.query(Role).filter(Role.name == "student").first()
    user = User(email="student_map@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=student_role.id))
    db_session.commit()
    token = create_access_token(data={"sub": str(user.id)})

    resp = client.post(
        "/api/v1/exam-subjects",
        json={
            "exam_id": exam["id"],
            "subject_id": subject["id"],
            "weightage": 50.0,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 403, resp.text
