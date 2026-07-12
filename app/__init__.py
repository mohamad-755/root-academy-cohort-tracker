from flask import Flask

from config import Config


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)
    
    from app.extensions import db as sqlalchemy_db
    sqlalchemy_db.init_app(app)

    from app.extensions import migrate
    migrate.init_app(app, sqlalchemy_db)

    from app.mail import mail
    mail.init_app(app)

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