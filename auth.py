import sqlite3
from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user
from .models import users, clubs
from . import db
import os.path



auth = Blueprint('auth', __name__)



def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/login')
def login():
    if request.method == "GET":
        return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    session['email'] = email
        #session['id'] = request.form['id']

    remember = True if request.form.get('remember') else False
    user = users.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login_post')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/test')

def test():
    conn = get_db_connection()
    clubs = conn.execute('SELECT * FROM clubs').fetchall()
    conn.close()
    return render_template('test.html', clubs=clubs)
    
@auth.route('/signup')

def signup():
    if request.method == "GET":
        conn = get_db_connection()
        clubs = conn.execute('SELECT * FROM clubs').fetchall()
        conn.close()
        return render_template('signup.html', clubs=clubs)

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    prenom = request.form.get('prenom')
    club = request.form.get('club')
    sexe = request.form.get('sexe')

    user = users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup_post'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = users(email=email, name=name, password=generate_password_hash(password, method='scrypt'), prenom=prenom, club=club, sexe=sexe)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login_post'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
