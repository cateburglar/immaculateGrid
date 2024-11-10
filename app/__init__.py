import os

from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from . import csi3335f2024 as cfg

# Init extensions
db = SQLAlchemy()
login_manager = LoginManager()


def login_required_middleware():
    if not current_user.is_authenticated and request.endpoint not in [
        "home_routes.login",
        "home_routes.signup",
    ]:
        return redirect(url_for("home_routes.login"))


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{cfg.mysql['user']}:{cfg.mysql['password']}@{cfg.mysql['host']}/{cfg.mysql['db']}"
    )
    app.secret_key = os.urandom(24).hex()

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "home_routes.login"

    # Register middleware
    app.before_request(login_required_middleware)

    with app.app_context():
        # Register blueprints/routes
        from .models import User
        from .routes import allstarfull_routes, home_routes

        app.register_blueprint(home_routes, url_prefix="/")
        app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
