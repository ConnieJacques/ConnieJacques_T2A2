from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.books import Book
from schemas.book_schema import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
books = Blueprint('books', __name__, url_prefix="/books")


# Query database to get all the books from the book table.
# Public access - no authentication required
@books.route("/", methods=["GET"])
@exception_handler
def get_all_books():
    books = db.session.query(Book).all()

    # Return an error if no books are located
    if not books:
        return abort(400, description="Book table not located.") 

    result = books_schema.dump(books)
    return jsonify(result)


# Query the books table with a query string
@books.route("/search", methods=["GET"])
@exception_handler
def search_books():
    try:
        # Create a list to hold the results
        books_list = []

        # Query database by book title
        if request.args.get('title'):
            books_list = db.session.query(Book).filter_by(title=request.args.get('title'))
        # Query database by length of book
        elif request.args.get('length'):
            books_list = db.session.query(Book).filter_by(length=request.args.get('length'))
        # Query database by an author_id and return all books written by that author
        elif request.args.get('author_id'):
            books_list = db.session.query(Book).filter_by(author_id=request.args.get('author_id'))
        # Query database by publisher_id and return all books published by that publisher
        elif request.args.get('publisher_id'):
            books_list = db.session.query(Book).filter_by(publisher_id=request.args.get('publisher_id'))
        # Return an error if the query string is invalid
        elif books_list == []:
            return abort(400, description="Missing or invalid query string.")

        # Return books_list in JSON format
        result = books_schema.dump(books_list)
        return jsonify(result)
    # Catch errors if an invalid query is attempted
    except exc.DataError:
        return abort(400, description="Invalid parameter in query string")
    

# Query the books table with a query string
@books.route("/searchby", methods=["GET"])
@exception_handler
def search_book():
    try:
        # Create a list to hold the results
        book_list = []

        # Query database by a book's unique isbn number
        if request.args.get('isbn'):
            book_list = db.session.query(Book).filter_by(isbn=request.args.get('isbn')).first()
        # Query database by book_id
        elif request.args.get('id'):
            book_list = db.session.query(Book).filter_by(id=request.args.get('id')).first()

        # Return book_list in JSON format
        result = book_schema.dump(book_list)
        return jsonify(result)
    # Catch errors if an invalid query is attempted
    except exc.DataError:
        return abort(400, description="Invalid parameter in query string")


# Allow an admin user to add a new book to the book table
# Requires details for the new book in the request body
# Must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@books.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_book():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a book.")

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
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")
    

# Allow an admin user to change data for an entry in the book table
# Requires details of the change to a book in the request body
# Request body must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@books.route("/update/<int:book_id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_book(book_id):
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add an author.")
        
        # Find the book by id
        book = Book.query.filter_by(id=book_id).first()
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
         return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")

    
# # Allow an admin user to delete an entry from the book table
# @books.route("/delete/<int:id>", methods=["DELETE"])
# @jwt_required()
# def delete_book(id):
#     try:
#         # Verify the user by getting their JWT identity querying the database with the id
#         verify_user = get_jwt_identity()
#         user = User.query.get(verify_user)

#         # If user is not already registered return an error message
#         if not user:
#             return abort(400, description="User not found. Please login.")
#         # Verify the user has admin privileges 
#         if user.admin != True:
#             return abort(403, description="You are not authorized to add a book.")
        
#         # Find the book by id
#         book = Book.query.filter_by(id=id).first()
#         if not book:
#             return abort(400, description= "Book could not be located in the database.")
        

#         # Commit the updated details to the book table
#         db.session.delete(book)
#         db.session.commit()

#         return jsonify(message="You have successfully removed this book from the database."), 200
#     except exceptions.ValidationError:
#         return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
#     except exc.IntegrityError:
#         return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/book/search} route with the isbn to located existing entry.")
#     except KeyError:
#         return abort(400, "Information incorrect in request body. Please ensure all fields are included.")
