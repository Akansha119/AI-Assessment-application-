"""RBAC service tests."""
from app.services.user_service import UserService
from app.permissions import ROLE_ADMIN, ROLE_STUDENT, has_permission


def test_has_permission_admin_star():
    assert has_permission({ROLE_ADMIN}, "exams:read") is True
    assert has_permission({ROLE_ADMIN}, "anything:at_all") is True


def test_has_permission_student():
    assert has_permission({ROLE_STUDENT}, "exams:read") is True
    assert has_permission({ROLE_STUDENT}, "exams:create") is False


def test_assign_and_remove_role(db_session):
    from app.models.role import Role
    from app.models.user import User

    svc = UserService(db_session)
    user = User(email="rbac@example.com", password_hash="x")
    db_session.add(user)
    db_session.commit()

    assert svc.assign_role(user.id, "student") is True
    assert has_permission({r.name for r in user.roles}, "exams:read") is True
    assert has_permission({r.name for r in user.roles}, "exams:create") is False

    assert svc.assign_role(user.id, "administrator") is True
    assert has_permission({r.name for r in user.roles}, "exams:create") is True

    assert svc.remove_role(user.id, "administrator") is True
    assert has_permission({r.name for r in user.roles}, "exams:create") is False
