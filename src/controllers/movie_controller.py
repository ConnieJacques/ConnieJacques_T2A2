from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc, desc, asc
from marshmallow import exceptions
from models.movies import Movie
from schemas.movie_schema import movie_schema, movies_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
movies = Blueprint('movies', __name__, url_prefix="/movies")


# Query database to get all the movies from the movie table. 
# Public access - no authentication required
@movies.route("/", methods=["GET"])
@exception_handler
def get_all_movies():
    movies = db.session.query(Movie).all()

    # Return an error if no movies are located
    if not movies:
        return abort(400, description="Movie table not located.") 
    
    result = movies_schema.dump(movies)
    return jsonify(result)


# Query the movies table with a query string
@movies.route("/search", methods=["GET"])
@exception_handler
def search_movies():
    try:
        # Create a list to hold the results
        movies_list = []

        # Query database by movie title
        if request.args.get('title'):
            movies_list = db.session.query(Movie).filter_by(title=request.args.get('title'))      
        # Query database by an director_id and return all movies directed by that director
        elif request.args.get('director_id'):
            movies_list = db.session.query(Movie).filter_by(director_id=request.args.get('director_id'))
        # Query database by an production_company_id and return all movies made by that production company
        elif request.args.get('production_company_id'):
            movies_list = db.session.query(Movie).filter_by(production_company_id=request.args.get('production_company_id'))
        # Query database by book_id and return all the movies adapted from that book
        elif request.args.get('book_id'):
            movies_list = db.session.query(Movie).filter_by(book_id=request.args.get('book_id'))

        # Return movies_list in JSON format
        result = movies_schema.dump(movies_list)
        return jsonify(result)
    # Catch errors if an invalid query is attempted
    except exc.DataError:
        return abort(400, description="Invalid parameter in query string")
    

# Query the movies table to return all movies sorted by length in ascending
@movies.route("/search/length", methods=["GET"])
@exception_handler
def sort_movies_length():
    movies = db.session.query(Movie).order_by(asc(Movie.length)).all()

    # Return an error if no movies are located
    if not movies:
            return abort(400, description="Movies not found.") 

    # Return movies JSON format
    result = movies_schema.dump(movies)
    return jsonify(result)   


# Query the movies table and return all movies sorted by box office ranking in descending order
@movies.route("/search/ranking", methods=["GET"])
@exception_handler
def sort_movies_ranking():
    movies = db.session.query(Movie).order_by(desc(Movie.box_office_ranking)).all()

    # Return an error if no movies are located
    if not movies:
            return abort(400, description="Movies not found.") 

    # Return movies JSON format
    result = movies_schema.dump(movies)
    return jsonify(result)  


# Query the movies table by movie_id
@movies.route("/search/<int:id>", methods=["GET"])
def search_movie_id(id):
    try:
        movie = db.session.query(Movie).filter_by(id=id).first()

        # Return an error if no movies are located
        if not movie:
            return abort(400, description= "Movie could not be located in the database.")

        # Return movies_list in JSON format
        result = movie_schema.dump(movie)
        return jsonify(result)
        # Catch errors if no results is returned or an invalid query is attempted
    except exc.DataError:
        return abort(400, description="Invalid parameter in query string")


# Allow an admin user to add a new movie to the movie table
# Request body must include:
# "title", "release_date", "length", "box_office_ranking", "book_id", "director_id", "production_company_id"
@movies.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_movie():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a movie.")

        # Add the new movie's details
        movie = Movie()
        movie_fields = movie_schema.load(request.json)
        movie.title = movie_fields["title"]
        movie.release_date = movie_fields["release_date"]
        movie.box_office_ranking = movie_fields["box_office_ranking"]
        movie.book_id = movie_fields["book_id"]
        movie.length = movie_fields["length"]
        movie.director_id = movie_fields["director_id"]
        movie.production_company_id = movie_fields["production_company_id"]

        # Commit the new movie's details to the movie table
        db.session.add(movie)
        db.session.commit()

        return jsonify(message="You have added a movie to the table."), 200
    # Catch errors if an invalid query is attempted
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")

    
# Allow an admin user to change data for an entry in the movie table
# Requires details of the change to a movie in the request body
# Request body must include:
# "title", "release_date", "length", "box_office_ranking", "book_id", "director_id", "production_company_id" 
@movies.route("/update/<int:id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_movie(id):
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a movie.")
        
        # Find the movie by id
        movie = db.session.query(Movie).filter_by(id=id).first()
        if not movie:
            return abort(400, description= "Movie could not be located in the database.")
        
        # Add the new movie's details
        movie_fields = movie_schema.load(request.json)
        movie.title = movie_fields["title"]
        movie.release_date = movie_fields["release_date"]
        movie.box_office_ranking = movie_fields["box_office_ranking"]
        movie.book_id = movie_fields["book_id"]
        movie.length = movie_fields["length"]
        movie.director_id = movie_fields["director_id"]
        movie.production_company_id = movie_fields["production_company_id"]

        # Commit the updated details to the movie table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    # Catch errors if an invalid query is attempted
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")
 
    
  
# # Allow an admin user to delete an entry from the book table
@movies.route("/delete/<int:movie_id>", methods=["DELETE"])
# @exception_handler
@jwt_required()
def delete_movie(movie_id):
    # Verify the user by getting their JWT identity and querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)
    
    # If the user's id from the token does not match any record in the database, return an error
    if not user:
        return abort(400, description="User not found.")
    if user.admin != True:
        return abort(403, description="You are not authorized to add an author.")
    
    # Find the book by id
    movie = db.session.query(Movie).filter_by(id=movie_id).first()

    if not movie:
        return abort(400, description= "Book could not be located in the database.")
    

    # Commit the updated details to the book table
    db.session.delete(movie)
    db.session.commit()

    return jsonify(message="You have successfully removed this movie and associated information from the database."), 200

