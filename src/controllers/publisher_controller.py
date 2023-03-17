from flask import Blueprint, jsonify, request, abort
from app import db
from marshmallow import exceptions
from models.books import Publisher
from schemas.publisher_schema import publisher_schema, publishers_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
publishers = Blueprint('publishers', __name__, url_prefix="/publishers")


# Query database to get all the publishers from the publisher table. 
# Public access - no authentication required
@publishers.route("/", methods=["GET"])
@exception_handler
def get_all_publishers():
    publishers = db.session.query(Publisher).all()
    result = publishers_schema.dump(publishers)
    return jsonify(result)


# Query the publishers table with a query string to get publisher by name
@publishers.route("/search/name/<string:name>", methods=["GET"])
@exception_handler
def search_publisher_name(name):
    # Query database by publisher_id
    publisher = db.session.query(Publisher).filter_by(publisher_name=name).first()

    # Return an error if name is invalid
    if not publisher:
        return abort(400, description="Publisher not found.")

    # Return a publishers in JSON format
    result = publisher_schema.dump(publisher)
    return jsonify(result)


# Query the publishers table with publisher_id
@publishers.route("/search/<int:id>", methods=["GET"])
@exception_handler
def search_publisher_id(id):
    # Query database by publisher_id
    publisher = db.session.query(Publisher).filter_by(id=id).first()

    # Return error message if the id passed is invalid
    if not publisher:
        return jsonify(message="Invalid query string.")

    # Return a publisher in JSON format
    result = publisher_schema.dump(publisher)
    return jsonify(result)


# Allow an admin user to add a new publisher to the publisher table
# Requires details for the new publisher in the request body
# Must include "publisher_name"
@publishers.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_publisher():
    try:
         # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        # If the user does not have admin privileges return an error
        if user.admin != True:
            return abort(403, description="You are not authorized to add a Publisher.")

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
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")    


# Allow an admin user to change data for an entry in the publisher table
# Requires details of the change to a publisher in the request body
# Must include "publisher_name"
@publishers.route("/update/<int:publisher_id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_publisher(publisher_id):
    try:
         # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        # If the user does not have admin privileges return an error
        if user.admin != True:
            return abort(403, description="You are not authorized to add a publisher.")
        
        # Find the publisher by id
        publisher = db.session.query(Publisher).filter_by(id=publisher_id).first()
        if not publisher:
            return abort(400, description= "Publisher could not be located in the database.")
        
        # Add the new publisher's details
        publisher_fields = publisher_schema.load(request.json)
        publisher.publisher_name = publisher_fields["publisher_name"]

        # Commit the updated details to the publisher table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")