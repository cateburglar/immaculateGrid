from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.models import Teams
from app.static.constants import LEAGUES_MAPPING


class LeaguesForm(FlaskForm):
    league_name = SelectField(
        "League",
        choices=[("", "Select a league")]
        + [(key, value) for key, value in LEAGUES_MAPPING.items()],
        validators=[DataRequired()],
    )

    yearID = SelectField(
        "Year",
        choices=[],
        id="year-select",
        validators=[DataRequired()],
        validate_choice=False,
    )

    submit = SubmitField("Get League Standings")

    @staticmethod
    def get_years_for_league(lgID):
        # Query the database to get the available years for the selected team
        available_years = (
            db.session.query(Teams.yearID)
            .filter(Teams.lgID == lgID)
            .distinct()
            .order_by(desc(Teams.yearID))
            .all()
        )
        years = [year[0] for year in available_years]
        return years
