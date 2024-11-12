from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db

from ..models import User

admin_routes = Blueprint("admin_routes", __name__, template_folder="templates")


@admin_routes.route("/users")
def users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


@admin_routes.route("/users/<int:user_id>")
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)
