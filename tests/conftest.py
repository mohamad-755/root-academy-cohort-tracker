import pytest

from app import create_app
from app.extensions import db as sqlalchemy_db


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
        sqlalchemy_db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth(client):
    class AuthActions:
        def create_student(self, name="Test Student", email="student@example.com", access_code="ROOT2026"):
            client.post(
                "/admin/login",
                data={"admin_code": "test-admin-code"},
                follow_redirects=True,
            )

            response = client.post(
                "/admin/students/new",
                data={
                    "name": name,
                    "email": email,
                    "access_code": access_code,
                },
                follow_redirects=True,
            )

            client.get("/admin/logout", follow_redirects=True)
            return response

        def login(self, email="student@example.com", access_code="ROOT2026"):
            return client.post(
                "/login",
                data={
                    "email": email,
                    "access_code": access_code,
                },
                follow_redirects=True,
            )

        def logout(self):
            return client.get("/logout", follow_redirects=True)

    return AuthActions()
