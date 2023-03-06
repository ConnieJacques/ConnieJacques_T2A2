from app import db


# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), unique=True, nullable=False)
    length = db.Column(db.String(), nullable=False)
    first_publication_date = db.Column(db.DateTime, nullable=False)
    copies_published = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    movie = db.relationship('Movie', backref='movie', cascade="all, delete")


# Define Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    published_name = db.Column(db.String(), nullable=False)
    collaboration = db.Column(db.Boolean)
    pen_name = db.Column(db.Boolean)
    collaborator_name = db.Column(db.String())
    author = db.relationship('Book', backref='author', cascade="all, delete")


# Define Publisher model
class Publisher(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(), nullable=False)
    publisher = db.relationship('Book', backref='publisher', cascade="all, delete")