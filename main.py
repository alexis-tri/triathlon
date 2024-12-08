from flask import Blueprint, render_template, request, url_for, flash, redirect, g, session, Flask
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
    print(db_path)
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
    
    # Fetch all races
    races = conn.execute('SELECT * FROM courses').fetchall()
    
    # Get the club of the current user
    cursor = conn.execute("SELECT club FROM users WHERE email = ?", (session["email"],))
    user_club = cursor.fetchone()

    if user_club:
        user_club = user_club['club']
        # Fetch favorite races for the user's club only
        favorite_races = conn.execute('''
            SELECT c.id, c.name, c.date, c.distance
            FROM club_favorites cf
            JOIN courses c ON cf.course_id = c.id
            WHERE cf.club_id = ?
        ''', (user_club,)).fetchall()
    else:
        favorite_races = []  # No favorites if no club found

    conn.close()
    
    return render_template('races.html', races=races, favorite_races=favorite_races)
@main.route('/courses/<int:race_id>')
def course(race_id):
    race = get_post_race(race_id)
    #return render_template('race.html', race=race)
        # Get the club of the current user
    conn = get_db_connection()
    cursor = conn.execute("SELECT club FROM users WHERE email = ?", (session["email"],))
    user_club = cursor.fetchone()

    if user_club:
        user_club = user_club['club']
    else:
        user_club = None

    # Get users participating in the same race and club along with their chosen distances
    participants = []
    if user_club:
        participants = conn.execute('''
            SELECT u.email, u.name, u.prenom, uc.distance
            FROM users_courses uc
            JOIN users u ON uc.user_id = u.id
            WHERE uc.course_id = ? AND u.club = ?
        ''', (race_id, user_club)).fetchall()

    #Get user is an admin or not
    cursor = conn.execute("SELECT is_admin FROM users WHERE email = ?", (session["email"],))
    user = cursor.fetchone()
    is_admin = user['is_admin'] if user else 0  # Default to 0 if user not found

    #Get user is participating
    cursor = conn.execute(
        '''
        SELECT * FROM users_courses 
        WHERE user_id = (SELECT id FROM users WHERE email = ?) 
        AND course_id = ? 
        ''',
        (session["email"], race_id)
    )
    is_participating = cursor.fetchone() is not None

    #Get the race a race club or not
    cursor = conn.execute(
        '''
        SELECT * FROM club_favorites 
        WHERE club_id = (SELECT club FROM users WHERE email = ?) 
        AND course_id = ?
        ''',
        (session["email"], race_id)
    )
    is_favorite = cursor.fetchone() is not None

    conn.close()
    return render_template('race.html', race=race, participants=participants, is_participating=is_participating, is_admin=is_admin, is_favorite=is_favorite)

@main.route('/courses/<int:id>/participe', methods=('POST',))
def participe(id):
    post = get_post_race(id)
    conn = get_db_connection()

    cursor = conn.execute('SELECT distance FROM courses WHERE id = ?', (id,))
    course = cursor.fetchone()

    available_distances = course[0] if course else None  # Safeguard if course is None
    selected_distance = request.form.get('distance')  # Always fetch submitted distance

    # Step 3: Handle distance selection logic
    if available_distances:  # If there are multiple distances
        selected_distance = request.form.get('distance')

        if not selected_distance:
            flash("Choisis une distance")
            return redirect(url_for('main.courses', post=post))  # Prompt user to select a distance

        # Ensure the selected distance is valid
        valid_distances = available_distances.split(';')
        if selected_distance not in valid_distances:
            flash("Distance invalide !")
            return redirect(url_for('main.courses', post=post))

    else:
        selected_distance = "NULL"  # If no distances, set it to None

    # Step 4: Check if the user is already registered for this race with the same distance
    cursor = conn.execute(
        'SELECT * FROM users_courses WHERE user_id = (SELECT id FROM users WHERE email = ?) AND course_id = ? AND (distance IS ? OR distance = ?)',
        (session["email"], id, selected_distance, selected_distance))
    result = cursor.fetchone()

    if result:
        flash(f"Tu es déjà inscrit sur cette course.")
        return redirect(url_for('main.courses', post=post))  # Already registered

    # Step 5: Insert participation into user_courses table
    conn.execute(
        'INSERT INTO users_courses (user_id, course_id, distance) VALUES ((SELECT id FROM users WHERE email = ?), ?, ?)',
        (session["email"], id, selected_distance))
    print(id, selected_distance)
    conn.commit()
    conn.close()

    # Step 6: Flash success message and redirect
    if selected_distance == "NULL":
        flash(f"Ta participation à {post['name']} a bien été enregistrée.")  # No specific distance
    else:
        flash(f"Ta participation à {post['name']} sur la distance {selected_distance} a bien été enregistrée.")
    return redirect(url_for('main.courses', post=post))

@main.route('/courses/<int:id>/unparticipate', methods=['POST'])
def unparticipate(id):
    conn = get_db_connection()

    # Delete the participation record for the current user
    conn.execute(
        '''
        DELETE FROM users_courses 
        WHERE user_id = (SELECT id FROM users WHERE email = ?) 
        AND course_id = ? 
        ''',
        (session["email"], id)
    )
    conn.commit()
    conn.close()

    flash("You have successfully unregistered from the race.")
    return redirect(url_for('main.courses', id=id))

@main.route('/courses/<int:id>', methods=['POST'])
def mark_favorite(id):
    conn = get_db_connection()

    # Step 4: Check if the user is already registered for this race with the same distance
    cursor = conn.execute(
        'SELECT * FROM club_favorites WHERE club_id = (SELECT club FROM users WHERE email = ?) AND course_id = ?',
        (session["email"], id))
    result = cursor.fetchone()

    if result:
        flash(f"Cette course est déjà considérée comme une course club")
        return redirect(url_for('main.courses', id=id))  # Already registered
    # Check if the current user is an admin and fetch their club
    cursor = conn.execute("SELECT is_admin, club FROM users WHERE email = ?", (session["email"],))
    user = cursor.fetchone()
    conn.execute('''
    INSERT INTO club_favorites (club_id, course_id)
        VALUES (?, ?)
    ''', (user['club'], id))
    conn.commit()
    flash('Cette course est désormais une course club')
    conn.close()
    return redirect(url_for('main.courses', id=id))

@main.route('/courses/<int:id>/remove_favorite', methods=['POST'])
def remove_favorite(id):
    conn = get_db_connection()

    # Remove the race from the club's favorites
    conn.execute(
        '''
        DELETE FROM club_favorites 
        WHERE club_id = (SELECT club FROM users WHERE email = ?) 
        AND course_id = ?
        ''',
        (session["email"], id)
    )
    conn.commit()
    conn.close()

    flash('Course club supprimée.')
    return redirect(url_for('main.courses', id=id))