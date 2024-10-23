import os

from flask import Blueprint, jsonify

from app.services.csv_service import update_allstarfull_from_csv

allstarfull_routes = Blueprint("allstarfull_routes", __name__)


@allstarfull_routes.route("/upload_allstarfull_csv", methods=["POST"])
def upload_allstarfull_csv():
    # Define the path to the CSV file
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "..", "static", "csv", "AllstarFull.csv")

    # Check if the file exists
    if not os.path.exists(csv_file_path):
        return jsonify({"error": "Allstarfull.csv not found"}), 404

    # Process the CSV file
    try:
        update_allstarfull_from_csv(csv_file_path)
        return jsonify({"message": "File processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
