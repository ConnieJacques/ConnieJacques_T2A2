from app import db

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    watched = db.relationship('Watched', backref='watched', cascade="all, delete")
    read = db.relationship('Read', backref='read', cascade="all, delete")

