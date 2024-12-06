from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import ValidationError


def no_spaces(form, field):
    if " " in field.data:
        raise ValidationError("Username must not contain spaces.")


class UpdateForm(FlaskForm):
    nameFirst = StringField("First Name")
    nameLast = StringField("Last Name")
    username = StringField("Username")
    password = PasswordField("Current Password")
    submit = SubmitField("Update")
