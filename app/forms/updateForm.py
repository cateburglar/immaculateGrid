from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class UpdateForm(FlaskForm):
    nameFirst = StringField(
        "First Name",
    )
    nameLast = StringField(
        "Last Name",
    )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Current Password")
    new_password = PasswordField("New Password")
    submit = SubmitField("Update")
