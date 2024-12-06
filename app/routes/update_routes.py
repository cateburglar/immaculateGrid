import logging
import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import UpdateForm, UpdatePasswordForm

from ..models import User

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger for home routes
log_file_path = os.path.join(log_dir, "update_logs.log")
logger = logging.getLogger("update_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Configure custom logger for stats logs
stats_log_file_path = os.path.join(log_dir, "stats_logs.log")
stats_logger = logging.getLogger("stats_logger")
stats_logger.setLevel(logging.INFO)
stats_file_handler = logging.FileHandler(stats_log_file_path)
stats_file_handler.setFormatter(formatter)
stats_logger.addHandler(stats_file_handler)

update_routes = Blueprint("update_routes", __name__, template_folder="templates")


@update_routes.route("/", methods=["GET", "POST"])
def update_profile():
    form = UpdateForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=session["username"]).first()
        if user:
            if form.password.data == None:
                flash("Password must be provided to update info", "danger")
                return render_template("update_profile.html", form=form, user=user)

            # Ensure the password is correct
            if not check_password_hash(user.password, form.password.data):
                flash("Reset unsuccessful: Password is incorrect", "danger")
                return render_template("update_profile.html", form=form, user=user)

            nameFirst = form.nameFirst.data
            nameLast = form.nameLast.data
            username = form.username.data

            if nameFirst != "" and nameFirst != None:
                user.nameFirst = nameFirst

            if nameLast != "" and nameLast != None:
                user.nameLast = nameLast

            if username != "" and username != None:
                user.username = username
                session["username"] = username

            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("home_routes.home"))
        else:
            logger.info(
                f"Could not find existing user to update for {form.username.data}"
            )
            flash("Username is invalid, please try again", "danger")
    else:
        user = User.query.filter_by(username=session["username"]).first()
        return render_template("update_profile.html", form=form, user=user)


@update_routes.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=session["username"]).first()
        if user:

            # Ensure original password is correct
            if not check_password_hash(user.password, form.password.data):
                flash("Reset unsuccessful: Current Password is incorrect", "danger")
                return render_template("update_password.html", form=form)
            else:

                # Update the password
                hashed_password = generate_password_hash(
                    form.new_password.data, method="scrypt"
                )
                user.password = hashed_password
                db.session.commit()
                flash("Password reset successfully!", "success")
                return redirect(url_for("home_routes.home"))

    return render_template("update_password.html", form=form)
