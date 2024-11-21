from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.forms import DepthChartForm
from ..models import Fielding, Teams #batting stats doesnt exist yet...

depth_chart_routes = Blueprint("depth_chart_routes", __name__, template_folder="templates")


# Route to handle the form and depth chart generation
@depth_chart_routes.route("/", methods=["GET", "POST"])
def depth_chart():
    form = DepthChartForm()

    if form.validate_on_submit():
        teamName = form.teamName.data
        year = form.yearID.data

        #find teamID of given team name
        team_ID = Teams.query.filter_by(team_name=teamName).first()

        # Query the database for the player's batting stats for the given yearID and teamID
        players = Fielding.query.filter_by(yearID=year, teamID=team_ID).all()

        # Assuming you have a SQLAlchemy query to fetch the data
        players = (Fielding.query(playerID, position, )#PA.label('plate_appearances'))
                   .filter(teamID==team_ID, yearID==year)
                   .group_by(playerID, position).all())

        # Group players by position
        depth_chart_data = {}
        for player in players:
            position = player.position
            if position not in depth_chart_data:
                depth_chart_data[position] = []
            depth_chart_data[position].append(player)

        return render_template("depth_chart.html", form=form, yearID=year_id, teamID=teamName, depth_chart_data=depth_chart_data)

    return render_template("depth_chart_form.html", form=form)