from flask import Flask

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import db
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth)

    from app.curriculum import curriculum
    app.register_blueprint(curriculum)

    from app.submissions import submissions
    app.register_blueprint(submissions)

    from app.admin import admin
    app.register_blueprint(admin)

    return app