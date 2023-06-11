from flask import Flask, render_template, session
from app.Models import db

from app.Blueprints.User.routes import userBlueprint
from app.Blueprints.Task.routes import taskBlueprint
from app.Blueprints.Habit.routes import habitBlueprint
from app.Blueprints.Dashboard.routes import dashboardBlueprint

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@/{}?unix_socket={}".format(
    app.config["DATABASE_USERNAME"],
    app.config["DATABASE_PASSWORD"],
    app.config["DATABASE_NAME"],
    app.config["UNIX_SOCKET"],
)
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def homeRoute():
    return render_template("home.html")


@app.route("/about")
def aboutRoute():
    return render_template("about.html")


app.register_blueprint(dashboardBlueprint, url_prefix="/dashboard")
app.register_blueprint(userBlueprint, url_prefix="/user")
app.register_blueprint(taskBlueprint, url_prefix="/task")
app.register_blueprint(habitBlueprint, url_prefix="/habit")
