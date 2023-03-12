from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.books import Book
from schemas.book_schema import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
books = Blueprint('books', __name__, url_prefix="/books")


# Query database to get all the books from the books table. 
# Public access - no authentication required
@books.route("/", methods=["GET"])
def get_all_books():
    try:
        books = Book.query.all()
        result = books_schema.dump(books)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the books table with a query string
@books.route("/search", methods=["GET"])
def search_books():
    try:
        # Create a list to hold the results
        books_list = []

        # Query database by book title
        if request.args.get('title'):
            books_list = Book.query.filter_by(title=request.args.get('title'))
        # Query database by length of book
        elif request.args.get('length'):
            books_list = Book.query.filter_by(length=request.args.get('length'))
        # Query database by a book's unique isbn number
        elif request.args.get('isbn'):
            books_list = Book.query.filter_by(isbn=request.args.get('isbn')).first()
        # Query database by book_id
        elif request.args.get('id'):
            books_list = Book.query.filter_by(id=request.args.get('id')).first()
        # Query database by an author_id and return all books written by that author
        elif request.args.get('author_id'):
            books_list = Book.query.filter_by(author_id=request.args.get('author_id'))
        # Query database by publisher_id and return all published by that publisher
        elif request.args.get('publisher_id'):
            books_list = Book.query.filter_by(publisher_id=request.args.get('publisher_id'))

        # Return books_list in JSON format
        result = books_schema.dump(books_list)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new book to the book table
# Requires details for the new book in the request body
# Must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@books.route("/add", methods=["POST"])
@jwt_required()
def add_book():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a book.")
        else:
            # Add the new book's details
            book = Book()
            book_fields = book_schema.load(request.json)
            book.title = book_fields["title"]
            book.isbn = book_fields["isbn"]
            book.length = book_fields["length"]
            book.first_publication_date= book_fields["first_publication_date"]
            book.copies_published = book_fields["copies_published"]
            book.author_id = book_fields["author_id"]
            book.publisher_id = book_fields["publisher_id"]

            # Commit the new book's details to the book table
            db.session.add(book)
            db.session.commit()

            return jsonify(message="You have added a book to the table."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/book/search} route with the isbn to located existing entry.")
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")
    


# Allow an admin user to change data for an entry in the book table
# Requires details of the change to a book in the request body
# Request body must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@books.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a book.")
        
        # Find the book by id
        book = Book.query.filter_by(id=id).first()
        if not book:
            return abort(400, description= "Book could not be located in the database.")
        
        # Add the new book's details
        book_fields = book_schema.load(request.json)
        book.title = book_fields["title"]
        book.isbn = book_fields["isbn"]
        book.length = book_fields["length"]
        book.first_publication_date= book_fields["first_publication_date"]
        book.copies_published = book_fields["copies_published"]
        book.author_id = book_fields["author_id"]
        book.publisher_id = book_fields["publisher_id"]

        # Commit the updated details to the book table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/book/search} route with the isbn to located existing entry.")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")
    
# Allow an admin user to delete an entry from the book table
@books.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        # Verify the user has admin privileges 
        if user.admin != True:
            return abort(403, description="You are not authorized to add a book.")
        
        # Find the book by id
        book = Book.query.filter_by(id=id).first()
        if not book:
            return abort(400, description= "Book could not be located in the database.")
        

        # Commit the updated details to the book table
        db.session.delete(book)
        db.session.commit()

        return jsonify(message="You have successfully removed this book from the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/book/search} route with the isbn to located existing entry.")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")
