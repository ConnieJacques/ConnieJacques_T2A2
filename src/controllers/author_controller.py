from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.books import Author
from schemas.author_schema import author_schema, authors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
authors = Blueprint('authors', __name__, url_prefix="/authors")


# Query database to get all the authors from the author table. 
# Public access - no authentication required
@authors.route("/", methods=["GET"])
def get_all_authors():
    try:
        authors = Author.query.all()
        result = authors_schema.dump(authors)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the authors table with a query string
@authors.route("/search", methods=["GET"])
def search_authors():
    try:
        # Create a list to hold the results
        authors_list = []

        # Query database by name of the author
        if request.args.get('published_name'):
            authors_list = Author.query.filter_by(published_name=request.args.get('published_name'))
        # Query database by collaboration, if True or False
        elif request.args.get('collaboration'):
            authors_list = Author.query.filter_by(collaboration=request.args.get('collaboration'))
        # Query database by pen name, if True or False
        elif request.args.get('pen_name'):
            authors_list = Author.query.filter_by(pen_name=request.args.get('pen_name'))
        # Query database by the name of a collaborator
        elif request.args.get('collaborator_name'):
            authors_list = Author.query.filter_by(collaborator_name=request.args.get('collaborator_name'))

        # Return authors_list in JSON format
        result = authors_schema.dump(authors_list)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Query the authors table with author_id
@authors.route("/search/<int:id>", methods=["GET"])
def search_author(id):
    try:
        # Query database by author_id
        author = Author.query.filter_by(id=id).first()

        # Return authors in JSON format
        result = author_schema.dump(author)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new author to the author table
# Requires details for the new author in the request body
# Must include "published_name" and can include "collaboration, collaborator_name" and "pen_name"
@authors.route("/add", methods=["POST"])
@jwt_required()
def add_author():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a Author.")
        else:
            # Add the new author's details
            author = Author()
            author_fields = author_schema.load(request.json)
            author.published_name = author_fields["published_name"]
            author.collaboration = author_fields["collaboration"]
            author.collaborator_name = author_fields["collaborator_name"]
            author. pen_name = author_fields["pen_name"]

            # Commit the new author's details to the author table
            db.session.add(author)
            db.session.commit()

            return jsonify(message="You have added an author to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion.")
    # Return an error if the new entry already exists in the database
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")


# Allow an admin user to change data for an entry in the author table
# Requires details of the change to a author in the request body
# Must include "published_name" and can include "collaboration, collaborator_name" and "pen_name"
@authors.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_author(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a Author.")
        
        # Find the author by id
        author = Author.query.filter_by(id=id).first()
        if not author:
            return abort(400, description= "Author could not be located in the database.")
        
        # Add the new Author's details
        author_fields = author_schema.load(request.json)
        author.published_name = author_fields["published_name"]
        author.collaboration = author_fields["collaboration"]
        author.collaborator_name = author_fields["collaborator_name"]
        author. pen_name = author_fields["pen_name"]

        # Commit the updated details to the author table
        db.session.commit()

        return jsonify(message="You have successfully updated this author in the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")