from flask import Blueprint, render_template, redirect, url_for, jsonify, session, request
from app.Models import db
from app.Models.Habit import Habit
from datetime import datetime


habitBlueprint = Blueprint('habitBlueprint', __name__,
                           template_folder='pages', static_folder='static')

@habitBlueprint.route('/')
def habitHomeRoute():
    currUserHabits = Habit.query.filter_by(userID=session['userId']).all()

    for habit in currUserHabits:
        if ((datetime.now() - habit.lastDateUpdated).days > 1):
            habit.ableToBeUpdated = True
        
        else:
            habit.ableToBeUpdated = False

    db.session.commit()
    return render_template('habitHome.html', habits=currUserHabits)

@habitBlueprint.route('/createHabitData', methods=["POST"])
def createHabitDataRoute():
    if (request.method == "POST"):
        h = Habit(habit=request.form['habit'], dayGoal=request.form['dayGoal'], userID=session['userId'])
        db.session.add(h)
        db.session.commit()

    return redirect(url_for('habitBlueprint.habitHomeRoute'))

@habitBlueprint.route('/delete', methods=["POST"])
def deleteHabitRoute():
    json = request.get_json()
    db.session.delete(Habit.query.filter_by(id=json['id']).first())
    db.session.commit()
    return jsonify({'status': 1})