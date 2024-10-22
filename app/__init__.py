from flask import Flask

from app.config import Config

from .extensions import db
from .routes.index_routes import index_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints/routes
    app.register_blueprint(index_routes)

    return app
