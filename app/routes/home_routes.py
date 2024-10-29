from flask import render_template, flash, redirect, url_for, Blueprint
from app.forms.loginForm import LoginForm

home_bp = Blueprint("home_routes", __name__)

@home_bp.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html',title="SEA QUAIL BABY",message="SQL more like sea quail amiright?")

@home_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home_routes.home'))
    return render_template('login.html', title='Sign In', form=form)
