from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.movies import Director
from schemas.director_schema import director_schema, directors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
directors = Blueprint('directors', __name__, url_prefix="/directors")


# Query database to get all the directors from the director table. 
# Public access - no authentication required
@directors.route("/", methods=["GET"])
def get_all_directors():
    try:
        directors = Director.query.all()
        result = directors_schema.dump(directors)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the directors table with a query string to get director by name
@directors.route("/search/name/<string:name>", methods=["GET"])
def search_publisher_name(name):
    try:
        # Query database by publisher_id
        director = Director.query.filter_by(publisher_name=name).first()

        if not director:
            return abort(400, description="Director not found.")

        # Return directors in JSON format
        result = director_schema.dump(director)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Query the directors table with publisher_id to director
@directors.route("/search/<int:id>", methods=["GET"])
def search_publisher_id(id):
    try:
        # Query database by publisher_id
        director = Director.query.filter_by(id=id).first()

        if not director:
            return abort(400, description="Director not found.")

        # Return directors in JSON format
        result = publisher_schema.dump(director)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new director to the director table
# Requires details for the new director in the request body
# Must include "publisher_name"
@directors.route("/add", methods=["POST"])
@jwt_required()
def add_publisher():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a Director.")
        else:
            # Add the new director's details
            director = Director()
            publisher_fields = publisher_schema.load(request.json)
            director.publisher_name = publisher_fields["publisher_name"]

            # Commit the new director's details to the director table
            db.session.add(director)
            db.session.commit()

            return jsonify(message="You have added an director to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion.")
    # Return an error if the new entry already exists in the database
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")
    


# Allow an admin user to change data for an entry in the director table
# Requires details of the change to a director in the request body
# Must include "published_name" and can include "collaboration, collaborator_name" and "pen_name"
@directors.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_director(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a director.")
        
        # Find the director by id
        director = Director.query.filter_by(id=id).first()
        if not director:
            return abort(400, description= "Director could not be located in the database.")
        
        # Add the new director's details
        director_fields = director_schema.load(request.json)
        director.published_name = director_fields["published_name"]
        director.collaboration = director_fields["collaboration"]
        director.collaborator_name = director_fields["collaborator_name"]
        director. pen_name = director_fields[" pen_name"]

        # Commit the updated details to the director table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")