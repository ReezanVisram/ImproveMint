from flask import Flask, render_template
from app.Models import db

from app.Blueprints.User.routes import userBlueprint
from app.Blueprints.Task.routes import taskBlueprint
from app.Blueprints.Habit.routes import habitBlueprint

app = Flask(__name__)
db.init_app(app)


if (app.config['ENV'] == 'production'):
    app.config.from_object('config.ProductionConfig')

elif (app.config['ENV'] == 'testing'):
    app.config.from_object('config.TestingConfig')

else:
    app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def homeRoute():
    return render_template('home.html')

app.register_blueprint(userBlueprint, url_prefix='/user')
app.register_blueprint(taskBlueprint, url_prefix='/task')
app.register_blueprint(habitBlueprint, url_prefix='/habit')
