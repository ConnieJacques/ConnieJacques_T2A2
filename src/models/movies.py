from app import db

# Define Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    length = db.Column(db.String(), nullable=False)
    box_office_ranking = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable=False)
    production_company_id = db.Column(db.Integer, db.ForeignKey('production_company.id'), nullable=False)
    watched = db.relationship('Watched', backref='watched', cascade="all, delete")

# Define Director model
class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(), nullable=False)
    director = db.relationship('Movie', backref='director', cascade="all, delete")


# Define ProductionCompany model
class ProductionCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    production_company = db.relationship('Movie', backref='production_company', cascade="all, delete")