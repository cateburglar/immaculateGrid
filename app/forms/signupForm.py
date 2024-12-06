from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    nameFirst = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    nameLast = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=5, max=30)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Create Account")
