from flask import render_template, flash, redirect, url_for
from app import create_app as app
from app.forms.loginForm import LoginForm

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',title="SEA QUAIL BABY",message="SQL more like sea quail amiright?")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)