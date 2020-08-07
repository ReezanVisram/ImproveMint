from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from app.Models import db

from app.Models.Task import Task

taskBlueprint = Blueprint('taskBlueprint', __name__,
                          template_folder='pages', static_folder='static')

@taskBlueprint.route('/')
def taskHomeRoute():
    allTasks = Task.query.filter_by(userID=session['userId']).all()

    currUserTasks = [i for i in allTasks if not i.completed]

    return render_template('taskHome.html', tasks=currUserTasks)

@taskBlueprint.route('/createTaskData', methods=["POST"])
def createTaskDataRoute():
    if (request.method == "POST"):
        currTask = Task(task=request.form['task'], userID=session['userId'])
        db.session.add(currTask)
        db.session.commit()
    return redirect(url_for('taskBlueprint.taskHomeRoute'))

@taskBlueprint.route('/markAsComplete', methods=["POST"])
def markTaskAsCompleteRoute():
    json = request.get_json()

    taskToUpdate = Task.query.filter_by(id=json['id']).first()
    taskToUpdate.completed = True
    db.session.commit()

    return jsonify({'status': 1})

@taskBlueprint.route('/completed')
def completedRoute():
    allTasks = Task.query.filter_by(userID=session['userId']).all()

    completedTasks = [i for i in allTasks if i.completed]
    return render_template('taskCompleted.html', tasks=completedTasks)

@taskBlueprint.route('/delete', methods=["POST"])
def deleteTaskRoute():
    json = request.get_json()

    taskToDelete = Task.query.filter_by(id=json['id']).first()
    db.session.delete(taskToDelete)
    db.session.commit()

    return jsonify({'status': 1})