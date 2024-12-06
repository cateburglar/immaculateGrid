from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    nameFirst = StringField("First Name", validators=[DataRequired()])
    nameLast = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Current Password")
    submit = SubmitField("Update")
