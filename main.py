from flask import Blueprint, render_template, request, url_for, flash, redirect, g, session
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from . import db
import os.path
import sqlite3

main = Blueprint('main', __name__)

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM communications WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_post_race(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM courses WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
'''
if current_user.is_authenticated():
    g.user = current_user.get_id()

user_email = session['email']
'''
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/communications')
def communications():
    conn = get_db_connection()
    comms = conn.execute('SELECT * FROM communications').fetchall()
    conn.close()
    return render_template('communications.html', comms=comms)

@main.route('/communications/<int:comm_id>')
def communication(comm_id):
    comm = get_post(comm_id)
    return render_template('communication.html', comm=comm)

@main.route('/communications/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO communications (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main.communications'))
    return render_template('createcommunication.html')

@main.route('/communications/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE communications SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('main.communications'))

    return render_template('editcommunication.html', post=post)

@main.route('/communications/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM communications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('main.communications'))

@main.route('/courses')
def courses():
    conn = get_db_connection()
    races = conn.execute('SELECT * FROM courses').fetchall()
    conn.close()
    return render_template('races.html', races=races)

@main.route('/courses/<int:race_id>')
def course(race_id):
    race = get_post_race(race_id)
    return render_template('race.html', race=race)

@main.route('/courses/<int:id>/participe', methods=('POST',))
def participe(id):
    post = get_post_race(id)
    conn = get_db_connection()
    getcourses = conn.execute("SELECT courses FROM users WHERE email = ? ", (session["email"],))
    if getcourses is not None:
        getcourses = str(getcourses)
        courses = [int(elem) for elem in getcourses.split(", ")] # transformation d'un string vers un array
        courses.append(id) # ajout d'un élément à l'array
        getcourses = "".join(f"{course}, " for course in courses)[:-2] # opération inverse (array vers string)
    conn.execute("UPDATE users WHERE email = ? SET courses = ? ", (session["email"],),(courses))
    conn.commit()
    conn.close()
    flash(f"Votre participation ({getcourses}) a été enregistrée à {post["name"]}.")
    return redirect(url_for('main.courses', post=post))
