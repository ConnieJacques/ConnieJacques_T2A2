from app import db, bcrypt
from flask import Blueprint
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
        first_name = "Admin",
        surname = "User",
        email = "fakeadmin@email.com",
        password = bcrypt.generate_password_hash("Pass1234").decode("utf-8"),
        admin = True
    )
    db.session.add(admin)

    admin2 = User(
        first_name = "Another Admin",
        surname = "Another User",
        email = "adminemail@email.com",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
        admin = True
    )
    db.session.add(admin2)

    user1 = User(
        first_name = "Jane",
        surname = "Doe",
        email = "email1@email.com",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
        admin = False
    )
    db.session.add(user1)

    user2 = User(
        first_name = "John",
        surname = "Smith",
        email = "email@email.com",
        password = bcrypt.generate_password_hash("12345678").decode("utf-8"),
        admin = False
    )
    db.session.add(user2)
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

    author3 = Author(
        published_name = "Stephen King and Peter Straub",
        pen_name = False,
        collaboration = True,
        collaborator_name = "Peter Straub"
    )
    db.session.add(author3)


    # Seed publisher next as needed for book table
    publisher1 = Publisher(
        publisher_name = "Doubleday"
    )
    db.session.add(publisher1)

    publisher2 = Publisher(
        publisher_name = "Signet Books"
    )
    db.session.add(publisher2)

    publisher3 = Publisher(
        publisher_name = "Viking"
    )
    db.session.add(publisher3)
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

    the_talisman = Book(
        title = "The Talisman",
        isbn = "0670691992",
        length = "646",
        first_publication_date = "1984-11-08",
        copies_published = "1250",
        author_id = author3.id,
        publisher_id = publisher3.id
    )
    db.session.add(the_talisman)

    pet_sematary = Book(
        title = "Pet Sematary",
        isbn = "0805775129",
        length = "374",
        first_publication_date = "1983-11-14",
        copies_published = "250000",
        author_id = author1.id,
        publisher_id = publisher1.id
    )
    db.session.add(pet_sematary)
    db.session.commit()


    # Seed director table next as needed for movie table
    director1 = Director(
        director_name = "Brian De Palma"
    )
    db.session.add(director1)

    director2 = Director(
        director_name = "Stanley Kubrick"
    )
    db.session.add(director2)

    director3 = Director(
        director_name = "Mary Lambert"
    )
    db.session.add(director3)
    db.session.commit()


    # Seed production_company table next as needed for movie table
    production1 = ProductionCompany(
        name = "Red Bank Films"
    )
    db.session.add(production1)

    production2 = ProductionCompany(
        name = "Warner Bros. Pictures"
    )
    db.session.add(production2)

    production3 = ProductionCompany(
        name = "Paramount Pictures"
    )
    db.session.add(production3)
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

    the_shining_movie = Movie(
        title = "The Shining",
        release_date = "1980-05-23",
        length = "144",
        box_office_ranking = 10123,
        book_id = the_shining.id,
        director_id = director2.id,
        production_company_id = production2.id 	
    )
    db.session.add(the_shining_movie)

    pet_sematary_movie = Movie(
        title = "Pet Sematary",
        release_date = "1989-04-21",
        length = "103",
        box_office_ranking = 26006,
        book_id = pet_sematary.id,
        director_id = director3.id,
        production_company_id = production3.id 	
    )
    db.session.add(pet_sematary_movie)
    db.session.commit()


    # Seed read table
    read1 = Read(
        book_id = carrie.id,
        user_id = admin.id,
        rating = 7
    )
    db.session.add(read1)

    read2 = Read(
        book_id = the_stand.id,
        user_id = user2.id,
        rating = 9
    )
    db.session.add(read2)

    read3 = Read(
        book_id = the_shining.id,
        user_id = admin2.id,
        rating = 8
    )
    db.session.add(read3)
    db.session.commit()


    # Seed watched table
    watched1 = Watched(
        movie_id = carrie_movie.id,
        user_id = admin.id,
        rating = 7
    )
    db.session.add(watched1)

    # Seed watched table
    watched2 = Watched(
        movie_id = the_shining_movie.id,
        user_id = user1.id,
        rating = 5
    )
    db.session.add(watched2)

    # Seed watched table
    watched3 = Watched(
        movie_id = pet_sematary_movie.id,
        user_id = admin.id,
        rating = 9
    )
    db.session.add(watched3)
    db.session.commit()


    print("Tables Seeded.")


# Drop table CLI command - execute using "flask drop" on the command line
@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables Dropped.") 