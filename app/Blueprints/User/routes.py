from flask import Blueprint, redirect, render_template, request, url_for
from app.Models.User import User
from app.Models import db
from werkzeug.security import generate_password_hash, check_password_hash

userBlueprint = Blueprint('userBlueprint', __name__,
                          template_folder='pages', static_folder='static')

@userBlueprint.route('/signUp', methods=["GET"])
def signUpRoute():
    return render_template('signUp.html')

@userBlueprint.route('/signUpDataRoute', methods=["POST"])
def signUpDataRoute():
    if (User.query.filter_by(email=request.form['email']).first()):
        return render_template('signUp.html', error='A user with that email already exists.')
    

    print('Name sent is ' + request.form['name'])
    print('Email sent is ' + request.form['email'])
    print('Password sent is ' + request.form['password'])

    try:
        u = User(username=request.form['name'], email=request.form['email'], password=generate_password_hash(request.form['password'], method='sha256'))
        db.session.add(u)
        db.session.commit()
    
    except Exception as e:
        return render_template('signUp.html', error=e)

    return redirect(url_for('homeRoute'))
