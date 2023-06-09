from flask import Blueprint, session, render_template, redirect, url_for
from Models.User import User
from Models.Task import Task
from Models.Habit import Habit

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
