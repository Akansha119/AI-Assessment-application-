"""Pytest configuration: SQLite in-memory DB override for FastAPI dependency."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base, get_db, SessionLocal  # noqa: F401
from app.main import app

SQLITE_URL = "sqlite:////tmp/assessiq_pytest.db"


@pytest.fixture(scope="function")
def db_session():
    # Import all models so Base.metadata is fully populated.
    import app.models  # noqa: F401

    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    # Seed system roles for RBAC tests
    from app.models.role import Role

    test_session = SessionLocal(bind=engine)
    try:
        for name in ["student", "administrator", "question_reviewer", "ai_service"]:
            if not test_session.query(Role).filter(Role.name == name).first():
                test_session.add(Role(name=name, is_system=True))
        test_session.commit()
    finally:
        test_session.close()
    SessionLocal.configure(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
        SessionLocal.configure(bind=None)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
