from app.Models import db

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(256))
    datePosted = db.Column(db.DateTime, index=True, default=datetime.now)
    lastDateUpdated = db.Column(db.DateTime, index=True)
    dayGoal = db.Column(db.Integer)
    daysDone = db.Column(db.Integer, index=True, default=0)
    ableToBeUpdated = db.Column(db.Boolean, default=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))