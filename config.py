import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    ADMIN_CODE = os.environ.get("ADMIN_CODE", "dev-admin-code")
    DATABASE = os.path.join(os.path.dirname(__file__), "instance", "app.db")