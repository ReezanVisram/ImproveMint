from flask import Flask, render_template
from app.Models import db

from app.Blueprints.User.routes import userBlueprint
from app.Blueprints.Task.routes import taskBlueprint
from app.Blueprints.Habit.routes import habitBlueprint
from app.Blueprints.Dashboard.routes import dashboardBlueprint

app = Flask(__name__)
if (app.config['ENV'] == 'production'):
    app.config.from_object('config.ProductionConfig')

elif (app.config['ENV'] == 'testing'):
    app.config.from_object('config.TestingConfig')

else:
    app.config.from_object('config.DevelopmentConfig')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(app.config['DATABASE_USERNAME'], app.config['DATABASE_PASSWORD'], app.config['DATABASE_HOST'], app.config['DATABASE_NAME'])
db.init_app(app)






@app.route('/')
def homeRoute():
    return render_template('home.html')

app.register_blueprint(dashboardBlueprint, url_prefix='/dashboard')
app.register_blueprint(userBlueprint, url_prefix='/user')
app.register_blueprint(taskBlueprint, url_prefix='/task')
app.register_blueprint(habitBlueprint, url_prefix='/habit')
