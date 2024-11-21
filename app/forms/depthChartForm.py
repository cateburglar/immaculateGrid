from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DepthChartForm(FlaskForm):
    teamName = StringField("Team Name", validators=[DataRequired()])
    yearID = IntegerField("Year", validators=[DataRequired()])
    submit = SubmitField("Generate Depth Chart")
