from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.forms import DepthChartForm
from .. import db
from dbSetup.models.tables import *

depth_chart_routes = Blueprint("depth_chart_routes", __name__, template_folder="templates")


# Route to handle the form and depth chart generation
@depth_chart_routes.route("/", methods=["GET", "POST"])
def depth_chart():
    form = DepthChartForm()

    if form.validate_on_submit():
        teamName = form.teamName.data
        year = form.yearID.data
        positionStat = form.positionStats.data
        pitcherStat = form.pitcherStats.data
        flag=False

        #find teamID of given team name
        team = db.session.query(Teams).filter_by(team_name=teamName).first()
        if not team:
            flag=True
            flash("team not found", "danger")
        if year < 1871 or year > 2023:
            flag=True
            flash("year must be >= 1871 and <= 2023", "danger")
        
        if flag:
            return render_template("depth_chart.html", form=form)
        
        team_ID = team.teamID

        # Query the database for the player's batting stats for the given yearID and teamID
        #THIS WILL BE REPLACED BY BATTING STATS EVENTUALLY TODO
        players = db.session.query(Fielding).filter_by(yearID=year, teamID=team_ID).all()
        if not players:
            flash("No players found for the selected team and year.", "info")
            return render_template("depth_chart.html", form=form)

        # Group players by position
        depth_chart_data = {}
        for player in players:
            position = player.position
            if position not in depth_chart_data:
                depth_chart_data[position] = []
            #THIS WILL CONTAIN BATTING STATS TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            depth_chart_data[position].append(player)


        # Query the database for batting leaders---- TODO will be modded!!!!!!!!!!!!!!!!
        batting_leaders = []
        batting_leaders = db.session.query(Batting).filter_by(yearID=year, teamID=team_ID).order_by(
            Batting.b_2B.desc(),
        ).limit(5).all()  # Adjust limit as needed

        # Query the database for pitching leaders ----- TODO WILL BE MODDED !!!!!!!!!!!!!!!
        pitching_leaders = db.session.query(
            Pitching.playerID,
            Pitching.p_W,
            Pitching.p_L,
            Pitching.p_SO
        ).filter_by(yearID=year, teamID=team_ID).order_by(
            Pitching.p_W.desc(),
            Pitching.p_L.asc(),
            Pitching.p_SO.desc()
        ).limit(5).all()  # Adjust limit as needed

        return render_template(
             "depth_chart.html", 
             form=form, 
             yearID=year, 
             teamName=teamName, 
             depth_chart_data=depth_chart_data,
             batting_leaders=batting_leaders,
             pitching_leaders=pitching_leaders
        )

    return render_template("depth_chart.html", form=form)