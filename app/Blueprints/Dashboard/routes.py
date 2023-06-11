from flask import Blueprint, session, render_template, redirect, url_for
from app.Models.User import User
from app.Models.Task import Task
from app.Models.Habit import Habit

dashboardBlueprint = Blueprint(
    "dashboardBlueprint", __name__, template_folder="pages", static_folder="static"
)


@dashboardBlueprint.route("/")
def dashboardHomeRoute():
    currUser = User.query.filter_by(id=session["userId"]).first()
    currUserTasks = Task.query.filter_by(userID=session["userId"]).all()
    currUserHabits = Habit.query.filter_by(userID=session["userId"]).all()

    return render_template(
        "dashboard.html", name=currUser.username, tasks=currUserTasks, habits=currUserHabits
    )
