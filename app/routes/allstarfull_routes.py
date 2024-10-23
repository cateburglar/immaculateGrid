import os

from flask import Blueprint, jsonify

from app.services.allstarfull_service import get_all_entries_allstarfull

allstarfull_routes = Blueprint("allstarfull_routes", __name__)


def model_to_dict(model):
    """
    Convert a SQLAlchemy model instance to a dictionary.
    """
    return {
        column.name: getattr(model, column.name) for column in model.__table__.columns
    }


@allstarfull_routes.route("/getall", methods=["GET"])
def get_all():
    try:
        entries = get_all_entries_allstarfull()
        entries_dict = [model_to_dict(entry) for entry in entries]
        return jsonify(entries_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
