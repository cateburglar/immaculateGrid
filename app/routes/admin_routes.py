from flask import Blueprint, flash, redirect, render_template, url_for

from app import db

from ..decorators import admin_required
from ..models import User

admin_routes = Blueprint("admin_routes", __name__, template_folder="templates")


@admin_routes.route("/users")
@admin_required
def users():
    all_users = User.query.filter_by(privilege="USER").all()
    return render_template("users.html", users=all_users)


@admin_routes.route("/users/<int:user_id>")
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@admin_routes.route("/users/<int:user_id>/ban", methods=["POST"])
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.banned = True
    db.session.commit()
    flash(f"User {user.username} has been banned.", "success")
    return redirect(url_for("admin_routes.user_detail", user_id=user_id))


@admin_routes.route("/users/<int:user_id>/unban", methods=["POST"])
@admin_required
def unban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.banned = False
    db.session.commit()
    flash(f"User {user.username} has been unbanned.", "success")
    return redirect(url_for("admin_routes.user_detail", user_id=user_id))
