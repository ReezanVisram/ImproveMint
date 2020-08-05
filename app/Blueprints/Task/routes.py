from flask import Blueprint, render_template, redirect, url_for, session, request
from app.Models import db

from app.Models.Task import Task

taskBlueprint = Blueprint('taskBlueprint', __name__,
                          template_folder='pages', static_folder='static')

@taskBlueprint.route('/')
def taskHomeRoute():
    currUserTasks = Task.query.filter_by(userID=session['userId']).all()

    return render_template('taskHome.html', tasks=currUserTasks)

@taskBlueprint.route('/createTaskData', methods=["POST"])
def createTaskDataRoute():
    if (request.method == "POST"):
        currTask = Task(task=request.form['task'], userID=session['userId'])
        db.session.add(currTask)
        db.session.commit()
    return redirect(url_for('taskBlueprint.taskHomeRoute'))
