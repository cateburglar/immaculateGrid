from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.forms import DepthChartForm
from .. import db
from dbSetup.models import *

depth_chart_routes = Blueprint("depth_chart_routes", __name__, template_folder="templates")


# Route to handle the form and depth chart generation
@depth_chart_routes.route("/", methods=["GET", "POST"])
def depth_chart():
    form = DepthChartForm()

    if form.validate_on_submit():
        teamName = form.teamName.data
        year = form.yearID.data

        #find teamID of given team name
        team = db.session.query(Teams).filter_by(team_name=teamName).first()
        if not team:
            flash("team not found", "error")
            return render_template("depth_chart.html", form=form)
        
        team_ID = team.teamID
        # Query the database for the player's batting stats for the given yearID and teamID
        #THIS WILL BE REPLACED BY BATTING STATS EVENTUALLY
        players = db.session.query(Fielding).filter_by(yearID=year, teamID=team_ID).all()

        # Group players by position
        depth_chart_data = {}
        for player in players:
            position = player.position
            if position not in depth_chart_data:
                depth_chart_data[position] = []
            #THIS WILL CONTAIN BATTING STATS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            depth_chart_data[position].append(player )

        return render_template(
             "depth_chart.html", 
             form=form, 
             yearID=year, 
             teamID=teamName, 
             depth_chart_data=depth_chart_data
        )

    return render_template("depth_chart.html", form=form)