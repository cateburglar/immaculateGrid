import os

from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from . import csi3335f2024 as cfg

# Init extensions
db = SQLAlchemy()
login_manager = LoginManager()


# Makes sure users can only visit login and signup when not logged in
def login_required_middleware():
    # Define routes that are accessible without login
    allowed_routes = ["/login", "/signup"]

    # Allow access to static files
    if request.path.startswith("/static"):
        return  # No redirection for static files

    # Redirect logged-in users trying to access login or signup pages to the home page
    if current_user.is_authenticated and request.path in allowed_routes:
        return redirect(url_for("home_routes.home"))

    # Redirect non-authenticated users trying to access restricted routes to login
    if not current_user.is_authenticated and request.path not in allowed_routes:
        return redirect(url_for("home_routes.login"))


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{cfg.mysql['user']}:{cfg.mysql['password']}@{cfg.mysql['host']}/{cfg.mysql['db']}"
    )
    app.secret_key = os.urandom(24).hex()

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "home_routes.login"
    login_manager.blueprint_login_views = {None: "/login"}

    # Register middleware
    app.before_request(login_required_middleware)

    # After app has initialized, define blueprints and create tables
    with app.app_context():
        # Register blueprints/routes
        from .models import User
        from .routes import admin_routes, allstarfull_routes, home_routes

        app.register_blueprint(home_routes, url_prefix="/")
        app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")
        app.register_blueprint(admin_routes, url_prefix="/admin")

        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
