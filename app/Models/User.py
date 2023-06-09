from Models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), unique=False)
