from flask_login import UserMixin
from . import db


            
class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    prenom = db.Column(db.String(100))
    club = db.Column(db.String(100))
    sexe = db.Column(db.String(1000))

class clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    clubname = db.Column(db.String(1000), unique=True)
    adresse = db.Column(db.String(100))

class communications(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(1000))
    content = db.Column(db.String(100))
    created = db.Column(db.DateTime(1000))
    content = db.Column(db.String(100))