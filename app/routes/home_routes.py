from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from app.forms.loginForm import LoginForm

from ..models import User

home_routes = Blueprint("home_routes", __name__, template_folder="templates")


# /
@home_routes.route("/")
def home():
    return render_template(
        "home.html",
        title="Home",
        message="SQL more like sea quail amiright?",
    )


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
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for("home"))  # Redirect to protected home route

        flash("Invalid username or password", "danger")

    return render_template("login.html", title="Sign In", form=form)
