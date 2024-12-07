import os

from flask import Flask, flash, redirect, request, url_for
from flask_login import LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from . import csi3335f2024 as cfg

# Init extensions
db = SQLAlchemy()
login_manager = LoginManager()


def check_if_banned():
    if current_user.is_authenticated and current_user.banned:
        logout_user()
        flash("Your account has been banned.", "danger")
        return redirect(url_for("home_routes.login"))


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
    app.before_request(check_if_banned)

    # After app has initialized, define blueprints and create tables
    with app.app_context():
        # Register blueprints/routes
        from .routes import (
            admin_routes,
            grid_routes,
            home_routes,
            team_routes,
            update_routes,
        )

        app.register_blueprint(home_routes, url_prefix="/")
        app.register_blueprint(admin_routes, url_prefix="/admin")
        app.register_blueprint(grid_routes, url_prefix="/grid")
        app.register_blueprint(update_routes, url_prefix="/update")
        app.register_blueprint(team_routes, url_prefix="/teams")

        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
