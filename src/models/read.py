from app import db


# Define Watched joining table
class Read(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    # Define Foreign Keys
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)