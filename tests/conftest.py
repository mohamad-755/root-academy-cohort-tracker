import pytest

from app import create_app
from app.db import init_db


@pytest.fixture
def app(tmp_path):
    test_db = tmp_path / "test.db"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": test_db,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(test_db).replace("\\", "/"),
            "MAIL_SUPPRESS_SEND": True,
            "ADMIN_CODE": "test-admin-code",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class AuthActions:
        def register(self, name="Test Student", email="student@example.com", cohort_code="ROOT2026"):
            return client.post(
                "/register",
                data={
                    "name": name,
                    "email": email,
                    "cohort_code": cohort_code,
                },
                follow_redirects=True,
            )

        def login(self, email="student@example.com", cohort_code="ROOT2026"):
            return client.post(
                "/login",
                data={
                    "email": email,
                    "cohort_code": cohort_code,
                },
                follow_redirects=True,
            )

        def logout(self):
            return client.get("/logout", follow_redirects=True)

    return AuthActions()