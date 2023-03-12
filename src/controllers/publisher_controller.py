from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.books import Publisher
from schemas.publisher_schema import publisher_schema, publishers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
publishers = Blueprint('publishers', __name__, url_prefix="/publishers")


# Query database to get all the publishers from the publisher table. 
# Public access - no authentication required
@publishers.route("/", methods=["GET"])
def get_all_publishers():
    try:
        publishers = Publisher.query.all()
        result = publishers_schema.dump(publishers)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the publishers table with a query string to get publisher by name
@publishers.route("/search/name/<string:name>", methods=["GET"])
def search_publisher_name(name):
    try:
        # Query database by publisher_id
        publisher = Publisher.query.filter_by(publisher_name=name).first()

        if not publisher:
            return abort(400, description="Publisher not found.")

        # Return publishers in JSON format
        result = publisher_schema.dump(publisher)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Query the publishers table with publisher_id to publisher
@publishers.route("/search/<int:id>", methods=["GET"])
def search_publisher_id(id):
    try:
        # Query database by publisher_id
        publisher = Publisher.query.filter_by(id=id).first()

        if not publisher:
            return abort(400, description="Publisher not found.")

        # Return publishers in JSON format
        result = publisher_schema.dump(publisher)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new publisher to the publisher table
# Requires details for the new publisher in the request body
# Must include "publisher_name"
@publishers.route("/add", methods=["POST"])
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
            return abort(403, description="You are not authorized to add a Publisher.")
        else:
            # Add the new publisher's details
            publisher = Publisher()
            publisher_fields = publisher_schema.load(request.json)
            publisher.publisher_name = publisher_fields["publisher_name"]

            # Commit the new publisher's details to the publisher table
            db.session.add(publisher)
            db.session.commit()

            return jsonify(message="You have added an publisher to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion.")
    # Return an error if the new entry already exists in the database
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")
    


# Allow an admin user to change data for an entry in the publisher table
# Requires details of the change to a publisher in the request body
# Must include "published_name" and can include "collaboration, collaborator_name" and "pen_name"
@publishers.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_publisher(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a publisher.")
        
        # Find the publisher by id
        publisher = Publisher.query.filter_by(id=id).first()
        if not publisher:
            return abort(400, description= "Publisher could not be located in the database.")
        
        # Add the new publisher's details
        publisher_fields = publisher_schema.load(request.json)
        publisher.published_name = publisher_fields["published_name"]
        publisher.collaboration = publisher_fields["collaboration"]
        publisher.collaborator_name = publisher_fields["collaborator_name"]
        publisher. pen_name = publisher_fields[" pen_name"]

        # Commit the updated details to the publisher table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")