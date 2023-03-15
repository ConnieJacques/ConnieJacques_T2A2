from app import db


# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    # Define relationship with read and watched tables
    watched = db.relationship('Watched', backref='user', cascade="all, delete")
    read = db.relationship('Read', backref='user', cascade="all, delete")