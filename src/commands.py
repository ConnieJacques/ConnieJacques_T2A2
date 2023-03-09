from app import db
from flask import Blueprint
from app import bcrypt
from models.users import User
from models.books import Book, Author, Publisher
from models.movies import Movie, Director, ProductionCompany
from models.read import Read
from models.watched import Watched


# Create database commands Blueprint
db_commands = Blueprint("db", __name__)


# Create table CLI command - execute using "flask create" on the command line
@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created.")


@db_commands .cli.command("seed")
def seed_db():

    #Seed the user table first
    admin = User(
        first_name = "Connie",
        surname = "Jacques",
        email = "fakeadmin@email.com",
        password = bcrypt.generate_password_hash("Pass1234").decode("utf-8"),
        admin = True
    )
    # Add and commit admin
    db.session.add(admin)
    db.session.commit()


    # Seed author table next as needed for book table
    author1 = Author(
        published_name = "Stephen King"
    )
    db.session.add(author1)

    author2 = Author(
        published_name = "Richard Bachman",
        pen_name = True
    )
    db.session.add(author2)
    db.session.commit()


    # Seed publisher next as needed for book table
    publisher1 = Publisher(
        publisher_name = "Doubleday"
    )
    db.session.add(publisher1)

    publisher2 = Publisher(
        publisher_name = "Signet Books"
    )
    db.session.add(publisher2)
    db.session.commit()


    # Seed book table next as needed for movie table
    carrie = Book(
        title = "Carrie",
        isbn = "0385086954",
        length = "199",
        first_publication_date = "1974-04-05",
        copies_published = "30000",
        author_id = author1.id,
        publisher_id = publisher1.id
    )
    db.session.add(carrie)

    salems_lot = Book(
        title = "'Salem's Lot",
        isbn = "0385007515",
        length = "439",
        first_publication_date = "1975-10-17",
        copies_published = "20000",
        author_id = author1.id,
        publisher_id = publisher1.id
    )
    db.session.add(salems_lot)

    the_shining = Book(
        title = "The Shining",
        isbn = "0385121679",
        length = "447",
        first_publication_date = "1977-01-28",
        copies_published = "25000",
        author_id = author1.id,
        publisher_id = publisher1.id
    )
    db.session.add(the_shining)
    
    rage = Book(
        title = "Rage",
        isbn = "0451076451",
        length = "211",
        first_publication_date = "1977-09-06",
        copies_published = "75000",
        author_id = author2.id,
        publisher_id = publisher2.id
    )
    db.session.add(rage)

    the_stand = Book(
        title = "The Stand",
        isbn = "0385121687",
        length = "823",
        first_publication_date = "1978-10-03",
        copies_published = "70000",
        author_id = author1.id,
        publisher_id = publisher1.id
    )
    db.session.add(the_stand)
    db.session.commit()


    # Seed director table next as needed for movie table
    director1 = Director(
        director_name = "Brian De Palma"
    )
    db.session.add(director1)
    db.session.commit()


    # Seed production_company table next as needed for movie table
    production1 = ProductionCompany(
        name = "Red Bank Films"
    )
    db.session.add(production1)
    db.session.commit()

    # Seed movie table next
    carrie_movie = Movie(
        title = "Carrie",
        release_date = "1976-11-03",
        length = "98",
        box_office_ranking = 22298,
        book_id = carrie.id,
        director_id = director1.id,
        production_company_id = production1.id
    )
    db.session.add(carrie_movie)
    db.session.commit()


    # Seed read table
    arbitrary_read = Read(
        book_id = carrie.id,
        user_id = admin.id,
        rating = 7
    )
    db.session.add(arbitrary_read)
    db.session.commit()


    # Seed watched table
    arbitrary_watched = Watched(
        movie_id = carrie_movie.id,
        user_id = admin.id,
        rating = 7
    )
    db.session.add(arbitrary_watched)
    db.session.commit()


# Drop table CLI command - execute using "flask drop" on the command line
@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped.") 