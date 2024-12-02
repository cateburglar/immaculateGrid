from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class DepthChartForm(FlaskForm):
    teamName = StringField("Team Name", render_kw={'placeholder': 'Enter team name'}, validators=[DataRequired()])
    yearID = IntegerField("Year", render_kw={'placeholder': 'Enter year'}, validators=[DataRequired()])

    # Dropdown for Position Stats with specific options
    #   choices: Each choice is a tuple 
    # where the first value is the option’s data 
    # (submitted value) and the second is the label
    #  displayed to the user.
    positionStats = SelectField(
        "Select projected stats displayed for Position Players:",
        choices=[
            ('PT', 'Playing Time'),
            ('PA', 'Plate Appearances'),
            ('WAR', 'Wins Above Replacement'),
            ('wRC+', 'Weighted Runs Created+'),
            ('wOBA', 'Weighted On-Base Average')
        ],
        validators=[DataRequired()]
    )

    # Dropdown for Pitcher Stats with specific options
    pitcherStats = SelectField(
        "Pitchers:",
        choices=[
            ('ERA', 'Earned Run Average'),
            ('PT', 'Playing Time'),
            ('IP', 'Innings Pitched'),
            ('WAR', 'Wins Above Replacement'),
            ('FIP', 'Fielding Independent Pitching')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Generate Depth Chart")