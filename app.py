from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
if app.config['ENV'] == "production":
    app.config.from_object("config.ProductionConfig")
    
elif app.config['ENV'] == "development":
    app.config.from_object('config.DevelopmentConfig')


Bootstrap(app)
db = SQLAlchemy(app)
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)

@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(256))
    taskDate = db.Column(db.DateTime, index=True, default=datetime.now)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit = db.Column(db.String(256))
    datePosted = db.Column(db.DateTime, index=True, default=datetime.now)
    lastDateUpdated = db.Column(db.DateTime, index=True)
    dayGoal = db.Column(db.Integer)
    daysDone = db.Column(db.Integer, index=True, default=0)
    ableToBeUpdated = db.Column(db.Boolean, default=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=32)])
    email = StringField("Email", validators=[InputRequired(), Email(message='Invalid Email')])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=32)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("Remember Me")

class TaskForm(FlaskForm):
    task = StringField("Task", validators=[InputRequired(), Length(max=256)])

class HabitForm(FlaskForm):
    habit = StringField("Habit", validators=[InputRequired(), Length(max=256)])
    dayGoal = IntegerField("Goal", validators=[InputRequired()])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()

    if form.validate_on_submit():
        hashedPassword = generate_password_hash(form.password.data, method='sha256')

        if User.query.filter_by(username=form.username.data).first() != None:
            return render_template('signup.html', form=form, error="A user with that username already exists")

        elif User.query.filter_by(email=form.email.data).first() != None:
            return render_template('signup.html', form=form, error="A user with that email already exists")

        else:
            new_user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('userCreated'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid Username or Password</h1>'
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(userID=current_user.id).all()
    habits = Task.query.filter_by(userID=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username, tasks=tasks, habits=habits)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/usercreated')
def userCreated():
    return render_template('usercreated.html')


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    tasks = Task.query.filter_by(userID=current_user.id).all()
    form = TaskForm()

    if form.validate_on_submit():
        newTask = Task(task=form.task.data, userID=current_user.id)
        db.session.add(newTask)
        db.session.commit()
        return redirect('/tasks')

    return render_template('task.html', name=current_user.username, tasks=tasks, form=form)

@app.route('/tasks/delete/<int:id>')
def deleteTask(id):
    taskToDelete = Task.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/tasks')

    except:
        return 'Could not delete task'

@app.route('/habits', methods=["GET", "POST"])
@login_required
def habits():
    habits = Habit.query.filter_by(userID=current_user.id).all()
    form = HabitForm()

    for i in range(len(habits)):
        if (datetime.utcnow() - habits[i].lastDateUpdated) > timedelta(1):
            habits[i].ableToBeUpdated = True

        else:
            habits[i].ableToBeUpdated = False

    try:
        db.session.commit()
        return render_template('habit.html', name=current_user.username, habits=habits, form=form)

    except:
        return '<h1>There was a problem updating the task</h1>'

    finally:
        if form.validate_on_submit():
            newHabit = Habit(habit=form.habit.data, userID=current_user.id, lastDateUpdated=datetime.utcnow())
            db.session.add(newHabit)
            db.session.commit()
            return redirect('/habits')

    return render_template('habit.html', name=current_user.username, habits=habits, form=form)

@app.route('/habits/updateday/<int:id>', methods=["GET", "POST"])
def updateHabitDay(id):
    if request.method == "POST":
        habitToBeUpdated = Habit.query.get_or_404(id)

        if (habitToBeUpdated.ableToBeUpdated == False):
            return redirect('/habits')

        else:
            habitToBeUpdated.lastDateUpdated = datetime.utcnow()
            habitToBeUpdated.daysDone += 1
            return redirect('/habits')

@app.route('/habits/delete/<int:id>', methods=["GET", "POST"])
def deleteHabit(id):
    habitToDelete = Habit.query.get_or_404(id)

    try:
        db.session.delete(habitToDelete)
        db.session.commit()
        return redirect('/habits')

    except:
        return '<h1>Could not delete habit</h1>'



if __name__ == '__main__':
    app.run()