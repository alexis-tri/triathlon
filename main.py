from flask import Blueprint, render_template, request, url_for, flash, redirect
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