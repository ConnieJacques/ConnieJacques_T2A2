from flask import Blueprint, jsonify, request, abort
from app import db
from marshmallow import exceptions
from models.movies import Director
from schemas.director_schema import director_schema, directors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
directors = Blueprint('directors', __name__, url_prefix="/directors")


# Query database to get all the directors from the director table. 
# Public access - no authentication required
@directors.route("/", methods=["GET"])
@exception_handler
def get_all_directors():
        directors = db.session.query(Director).all()
        result = directors_schema.dump(directors)
        return jsonify(result)


# Query the directors table with a query string to get a director by name
@directors.route("/search/name/<string:name>", methods=["GET"])
@exception_handler
def search_director_name(name):
    # Query database by publisher_id
    director = db.session.query(Director).filter_by(director_name=name).first()

    # Return an error if name is invalid
    if not director:
        return abort(400, description="Director not found.")

    # Return a director in JSON format
    result = director_schema.dump(director)
    return jsonify(result)


# Query the directors table with director_id
@directors.route("/search/<int:id>", methods=["GET"])
@exception_handler
def search_director_id(id):
    # Query database by publisher_id
    director = db.session.query(Director).filter_by(id=id).first()

    # Return error message if the id passed is invalid
    if not director:
        return jsonify(message="Invalid query string.")

    # Return a director in JSON format
    result = director_schema.dump(director)
    return jsonify(result)


# Allow an admin user to add a new director to the director table
# Requires details for the new director in the request body
# Must include "director_name"
@directors.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_director():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        # If the user does not have admin privileges return an error
        if user.admin != True:
            return abort(403, description="You are not authorized to add a director.")

        # Add the new director's details
        director = Director()
        director_fields = director_schema.load(request.json)
        director.director_name = director_fields["director_name"]

        # Commit the new director's details to the director table
        db.session.add(director)
        db.session.commit()

        return jsonify(message="You have added a director to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")
    

# Allow an admin user to change data for an entry in the director table
# Requires details of the change to a director in the request body
# Must include "publisher_name"
@directors.route("/update/<int:director_id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_director(director_id):
    try:
         # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a director.")
        
        # Find the director by id
        director = db.session.query(Director).filter_by(id=director_id).first()
        if not director:
            return abort(400, description= "Director could not be located in the database.")
        
        # Add the new director's details
        director_fields = director_schema.load(request.json)
        director.director_name = director_fields["director_name"]

        # Commit the updated details to the director table
        db.session.add(director)
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")