import os

from flask import Flask, render_template

from .routes import allstarfull_routes, home_routes


def create_app():
    app = Flask(__name__, template_folder="templates")

    # Register blueprints/routes
    app.register_blueprint(home_routes, url_prefix="/")
    app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")

    # Secret key for url_for Flask-WTF CSRF protection shtuff
    app.config["SECRET_KEY"] = os.urandom(24).hex()

    # Display home page by default
    @app.route("/")
    def home():
        return render_template(
            "home.html",
            title="Home",
            message="SQL more like sea quail amiright?",
        )

    return app


if __name__ == "__main__":
    app = create_app()
