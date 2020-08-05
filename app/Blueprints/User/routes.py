from flask import Blueprint, redirect, render_template, request, url_for, session
from app.Models.User import User
from app.Models import db
from werkzeug.security import generate_password_hash, check_password_hash

userBlueprint = Blueprint('userBlueprint', __name__,
                          template_folder='pages', static_folder='static')

@userBlueprint.route('/signUp', methods=["GET", "POST"])
def signUpRoute():
    return render_template('signUp.html', error=request.args.get('error'))

@userBlueprint.route('/signUpData', methods=["POST"])
def signUpDataRoute():
    if (User.query.filter_by(email=request.form['email']).first()):
        return redirect(url_for('userBlueprint.signUpRoute', error='Email Exists'))

    u = User(username=request.form['name'], email=request.form['email'], password=generate_password_hash(request.form['password'], method='sha256'))
    db.session.add(u)
    db.session.commit()
    

    return redirect(url_for('userBlueprint.loginRoute', error=None))

@userBlueprint.route('/login', methods=["GET", "POST"])
def loginRoute():
    return render_template('login.html', error=request.args.get('error'))

@userBlueprint.route('/loginData', methods=["POST"])
def loginDataRoute():
    currUser = User.query.filter_by(email=request.form['email']).first()
    if (currUser):
        if (check_password_hash(currUser.password, request.form['password'])):
            session['userId'] = currUser.id
            return redirect(url_for('dashboardBlueprint.dashboardHomeRoute'))

        return redirect(url_for('userBlueprint.loginRoute', error='Incorrect Password'))

    return redirect(url_for('userBlueprint.loginRoute', error='Incorrect Email'))

@userBlueprint.route('/logout')
def logoutRoute():
    print(session['userId'])
    session['userId'] = None
    return redirect(url_for('homeRoute'))


