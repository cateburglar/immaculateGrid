from flask import Flask

from app.csi3335f2024 import mysql

from .routes import allstarfull_routes, index_routes


def create_app():
    app = Flask(__name__)

    # Register blueprints/routes
    app.register_blueprint(index_routes)
    app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")

    return app
