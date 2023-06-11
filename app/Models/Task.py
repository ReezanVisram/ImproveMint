from app.Models import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(256))
    taskDate = db.Column(db.DateTime, index=True, default=datetime.now)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))
    completed = db.Column(db.Boolean, default=False)
