from flask import Blueprint, flash, redirect, render_template, request, url_for

grid_routes = Blueprint("grid_routes", __name__, template_folder="templates")


@grid_routes.route("/", methods=["GET", "POST"])
def get_player():
    if request.method == "POST":
        # Extract form data
        prompt1 = request.form.get("prompt1")
        prompt2 = request.form.get("prompt2")
        operator = request.form.get("operator")
        number = request.form.get("number")
        team = request.form.get("team")
        position = request.form.get("position")

        # Perform necessary actions with the extracted data
        # For example, query a database or perform calculations

        # Flash a message or redirect to another page
        flash("Form submitted successfully!", "success")
        return redirect(url_for("grid_routes.get_player"))

    return render_template("immaculate_grid.html")
