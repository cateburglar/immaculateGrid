import logging
import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, SignupForm

from ..models import User

# Ensure the logging directory exists
log_dir = os.path.join("app", "logging")
os.makedirs(log_dir, exist_ok=True)

# Configure custom logger
log_file_path = os.path.join(log_dir, "home_logs.log")
logger = logging.getLogger("home_routes_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

home_routes = Blueprint("home_routes", __name__, template_folder="templates")


# /
@home_routes.route("/")
def home():
    return render_template(
        "home.html",
        title="Home",
        message="SQL more like sea quail amiright?",
    )


@home_routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if not existing_user:
            # Hash the password
            hashed_password = generate_password_hash(
                form.password.data, method="scrypt"
            )

            # Create a new User instance
            new_user = User(
                nameFirst=form.nameFirst.data,
                nameLast=form.nameLast.data,
                username=form.username.data,
                password=hashed_password,
            )

            # Add the new user
            db.session.add(new_user)
            db.session.commit()

            # Log account creation
            logger.info(f"Account created: {new_user.username}")

            # Show a successs message and redirect to login
            flash("Account created successfully!", "success")
            login_user(new_user, remember=False)

            # Log login
            logger.info(f"Successful login: {new_user.username}")

            flash(f"Welcome, {new_user.username}!", "success")
            return redirect(url_for("home_routes.home"))

        else:
            logger.info(f"Duplicate account creation attempt for {form.username.data}")
            flash("Username is already taken, please try again", "danger")
    return render_template("signup.html", title="Sign Up", form=form)


# /login
@home_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user from the database
        user = User.query.filter_by(username=form.username.data).first()

        # Verify if the user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):
            # Log in the user and manage 'remember me' option
            login_user(user, remember=form.remember_me.data)
            logger.info(f"Successful login: {user.username}")
            session["username"] = user.username
            flash(f"Welcome, {user.nameFirst} {user.nameLast}!", "success")
            return redirect(url_for("home_routes.home"))

        logger.info(f"Failed login attempt: {form.username.data}")
        flash("Invalid username or password", "danger")

    return render_template("login.html", title="Sign In", form=form)


@home_routes.route("/logout")
def logout():
    logger.info(f"Logout: {session["username"]}")
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home_routes.login"))
