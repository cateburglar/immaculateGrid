from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.models import Teams
from app.static.constants import TEAM_MAPPINGS


class TeamSummaryForm(FlaskForm):
    teamName = SelectField(
        "Team Name",
        choices=[("", "Select a team")]
        + [(key, value) for key, value in TEAM_MAPPINGS.items()],
        validators=[DataRequired()],
    )

    submit = SubmitField("Get Team Summary")

    @staticmethod
    def get_years_for_team(team_name):
        # Query the database to get the available years for the selected team
        available_years = (
            db.session.query(Teams.yearID)
            .filter(Teams.team_name == team_name)
            .distinct()
            .all()
        )
        years = [year[0] for year in available_years]
        return years
