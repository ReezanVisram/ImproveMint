from app.Models import db
from datetime import datetime


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(256))
    lastDateUpdated = db.Column(db.DateTime, index=True, default=datetime.now)
    ableToBeUpdated = db.Column(db.Boolean, default=False)
    dayGoal = db.Column(db.Integer)
    daysDone = db.Column(db.Integer, index=True, default=1)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
