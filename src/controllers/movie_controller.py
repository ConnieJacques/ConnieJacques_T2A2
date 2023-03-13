from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.movies import Movie
from schemas.book_schema import book_schema, books_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
movies = Blueprint('movies', __name__, url_prefix="/movies")


# Query database to get all the movies from the movie table. 
# Public access - no authentication required
@movies.route("/", methods=["GET"])
def get_all_movies():
    try:
        movies = Movie.query.all()
        result = books_schema.dump(movies)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the movies table with a query string
@movies.route("/search", methods=["GET"])
def search_movies():
    try:
        # Create a list to hold the results
        books_list = []

        # Query database by movie title
        if request.args.get('title'):
            books_list = Movie.query.filter_by(title=request.args.get('title'))
        # Query database by length of movie
        elif request.args.get('length'):
            books_list = Movie.query.filter_by(length=request.args.get('length'))
        # Query database by an author_id and return all movies written by that author
        elif request.args.get('author_id'):
            books_list = Movie.query.filter_by(author_id=request.args.get('author_id'))
        # Query database by publisher_id and return all published by that publisher
        elif request.args.get('publisher_id'):
            books_list = Movie.query.filter_by(publisher_id=request.args.get('publisher_id'))

        # Return books_list in JSON format
        result = books_schema.dump(books_list)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")
    

# Query the movies table with a query string
@movies.route("/search/entry", methods=["GET"])
def search_movie():
    try:
        # Create a list to hold the results
        book_list = []

        # Query database by a movie's unique isbn number
        if request.args.get('isbn'):
            book_list = Movie.query.filter_by(isbn=request.args.get('isbn')).first()
        # Query database by book_id
        elif request.args.get('id'):
            book_list = Movie.query.filter_by(id=request.args.get('id')).first()

        # Return books_list in JSON format
        result = book_schema.dump(book_list)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new movie to the movie table
# Requires details for the new movie in the request body
# Must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@movies.route("/add", methods=["POST"])
@jwt_required()
def add_movie():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a movie.")
        else:
            # Add the new movie's details
            movie = Movie()
            book_fields = book_schema.load(request.json)
            movie.title = book_fields["title"]
            movie.isbn = book_fields["isbn"]
            movie.length = book_fields["length"]
            movie.first_publication_date= book_fields["first_publication_date"]
            movie.copies_published = book_fields["copies_published"]
            movie.author_id = book_fields["author_id"]
            movie.publisher_id = book_fields["publisher_id"]

            # Commit the new movie's details to the movie table
            db.session.add(movie)
            db.session.commit()

            return jsonify(message="You have added a movie to the table."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/movie/search} route with the isbn to located existing entry.")
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")
    


# Allow an admin user to change data for an entry in the movie table
# Requires details of the change to a movie in the request body
# Request body must include "title", "isbn", "length", "first_publication_date", "copies_published", "author_id" and "publisher_id"
@movies.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_movie(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to change the details of a movie.")
        
        # Find the movie by id
        movie = Movie.query.filter_by(id=id).first()
        if not movie:
            return abort(400, description= "Movie could not be located in the database.")
        
        # Add the new movie's details
        book_fields = book_schema.load(request.json)
        movie.title = book_fields["title"]
        movie.isbn = book_fields["isbn"]
        movie.length = book_fields["length"]
        movie.first_publication_date= book_fields["first_publication_date"]
        movie.copies_published = book_fields["copies_published"]
        movie.author_id = book_fields["author_id"]
        movie.publisher_id = book_fields["publisher_id"]

        # Commit the updated details to the movie table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/movie/search} route with the isbn to located existing entry.")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")
    
# Allow an admin user to delete an entry from the movie table
@movies.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_movie(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        # Verify the user has admin privileges 
        if user.admin != True:
            return abort(403, description="You are not authorized to add a movie.")
        
        # Find the movie by id
        movie = Movie.query.filter_by(id=id).first()
        if not movie:
            return abort(400, description= "Movie could not be located in the database.")
        

        # Commit the updated details to the movie table
        db.session.delete(movie)
        db.session.commit()

        return jsonify(message="You have successfully removed this movie from the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except exc.IntegrityError:
        return abort(400, description="ISBN number is already associated with another entry in the database. Please query the {/movie/search} route with the isbn to located existing entry.")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")
