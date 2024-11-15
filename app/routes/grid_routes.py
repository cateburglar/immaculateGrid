from flask import Blueprint, render_template

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


@grid_routes.route("/")
def prompts():
    return render_template("immaculate_grid.html")
