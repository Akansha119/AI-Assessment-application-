"""Exam pattern API tests."""
from app.core.security import create_access_token


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _make_admin(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    user = User(email="admin_pattern@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id))
    db_session.commit()
    return user


def _make_exam(client, db_session, token):
    resp = client.post(
        "/api/v1/exams",
        json={"code": "PATTERN_TEST", "name": "Pattern Test Exam"},
        headers=auth_headers(token),
    )
    return resp.json()


def test_create_exam_pattern_admin(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})
    exam = _make_exam(client, db_session, token)

    resp = client.post(
        "/api/v1/exam-patterns",
        json={
            "exam_id": exam["id"],
            "name": "Standard Pattern",
            "total_questions": 100,
            "marks_per_correct": 2.0,
            "negative_marking_penalty": 0.5,
            "duration_minutes": 120,
            "difficulty_distribution": '{"easy":30,"medium":50,"hard":20}',
            "is_default": True,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["name"] == "Standard Pattern"
    assert data["total_questions"] == 100
    assert data["marks_per_correct"] == 2.0
    assert data["is_default"] is True


def test_list_exam_patterns(client, db_session):
    user = _make_admin(client, db_session)
    token = create_access_token(data={"sub": str(user.id)})
    exam = _make_exam(client, db_session, token)

    client.post(
        "/api/v1/exam-patterns",
        json={
            "exam_id": exam["id"],
            "name": "List Pattern",
            "total_questions": 50,
            "marks_per_correct": 1.0,
            "negative_marking_penalty": 0.25,
            "duration_minutes": 60,
            "is_default": False,
        },
        headers=auth_headers(token),
    )

    resp = client.get(
        f"/api/v1/exam-patterns?exam_id={exam['id']}",
        headers=auth_headers(token),
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data) >= 1
    assert any(p["name"] == "List Pattern" for p in data)


def test_create_exam_pattern_student_forbidden(client, db_session):
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole

    # Create admin and exam first
    admin_role = db_session.query(Role).filter(Role.name == "administrator").first()
    admin = User(email="admin_for_pattern@example.com", password_hash="x")
    db_session.add(admin)
    db_session.commit()
    db_session.add(UserRole(user_id=admin.id, role_id=admin_role.id))
    db_session.commit()
    admin_token = create_access_token(data={"sub": str(admin.id)})

    exam = _make_exam(client, db_session, admin_token)

    # Now try as student
    student_role = db_session.query(Role).filter(Role.name == "student").first()
    user = User(email="student_pattern@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()
    db_session.add(UserRole(user_id=user.id, role_id=student_role.id))
    db_session.commit()
    token = create_access_token(data={"sub": str(user.id)})

    resp = client.post(
        "/api/v1/exam-patterns",
        json={
            "exam_id": exam["id"],
            "name": "Student Pattern",
            "total_questions": 50,
            "is_default": False,
        },
        headers=auth_headers(token),
    )
    assert resp.status_code == 403, resp.text
