from app import db


# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), unique=True, nullable=False)
    length = db.Column(db.String(), nullable=False)
    first_publication_date = db.Column(db.DateTime, nullable=False)
    copies_published = db.Column(db.String(), nullable=False)
    # Define Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    # Define relationship with read table
    read = db.relationship('Read', backref='book')


# Define Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    published_name = db.Column(db.String(), nullable=False)
    collaboration = db.Column(db.Boolean, default=False)
    pen_name = db.Column(db.Boolean, default=False)
    collaborator_name = db.Column(db.String())
    # Define relationship to book table
    author = db.relationship('Book', backref='author')


# Define Publisher model
class Publisher(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(), nullable=False)
    # Define relationship to book table
    publisher = db.relationship('Book', backref='publisher')