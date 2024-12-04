from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class DepthChartForm(FlaskForm):
    # Dropdown for Position Stats with specific options
    #   choices: Each choice is a tuple
    # where the first value is the option’s data
    # (submitted value) and the second is the label
    #  displayed to the user.
    positionStats = SelectField(
        "Select projected stats displayed for Position Players:",
        choices=[
            ("b_G", "Games Played"),
            ("b_PA", "Plate Appearances"),
            ("b_wRC", "Weighted Runs Created"),
            ("b_wOBA", "Weighted On-Base Average"),
            ("b_BB_percent", "Walk Percentage"),
        ],
        validators=[DataRequired()],
    )

    # Dropdown for Pitcher Stats with specific options
    pitcherStats = SelectField(
        "Pitchers:",
        choices=[
            ("p_ERA", "Earned Run Average"),
            #("p_PT", "Playing Time"),
            ("p_IP", "Innings Pitched"),
            #("WAR", "Wins Above Replacement"),
            ("p_FIP", "Fielding Independent Pitching"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Generate Depth Chart")
