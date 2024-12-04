import logging
import os

from flask import (
    Blueprint,
)
from app import db
from ..models import User
from werkzeug.security import generate_password_hash
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)
from app.forms import UpdateForm

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

@update_routes.route("/", methods=['GET', 'POST'])
def update_profile():
    form = UpdateForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if(user):
            nameFirst = form.nameFirst.data
            nameLast = form.nameLast.data
            password = form.password.data

            if(nameFirst):
                user.nameFirst = nameFirst
            if(nameLast):
                user.nameLast = nameLast
            if(password):
                # Hash the password
                hashed_password = generate_password_hash(
                    password, method="scrypt"
                )
                user.password = hashed_password

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('update_routes.update_profile'))
        else:
            logger.info(f"Could not find existing user to update for {form.username.data}")
            flash("Username is invalid, please try again", "danger")
    
    return render_template('update_profile.html', form=form)