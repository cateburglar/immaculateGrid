from flask import Blueprint, flash, redirect, render_template, url_for

from app.forms.loginForm import LoginForm

# the name "home_bp" is what we use to refer to the blueprint
# in url_for() statements-- to access the def login()
# url, you would do home_bp.login
home_routes = Blueprint("home_routes", __name__, template_folder="templates")


# so the url will be /home/login bc of the blueprint
@home_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # this is because we dont actually have a system for logging in yet
        flash(
            "Login requested for user {}, remember_me={}".format(
                form.username.data, form.remember_me.data
            )
        )

        # after they login, send them home but display messages
        return redirect(url_for("home"))

    return render_template("login.html", title="Sign In", form=form)
