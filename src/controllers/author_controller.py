from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.books import Author
from schemas.author_schema import author_schema, authors_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
authors = Blueprint('authors', __name__, url_prefix="/authors")


# Query database to get all the authors from the author table. 
# Public access - no authentication required
@authors.route("/", methods=["GET"])
@exception_handler
def get_all_authors():
    authors = db.session.query(Author).all()
    result = authors_schema.dump(authors)
    return jsonify(result)


# Query the authors table with a query string
@authors.route("/search", methods=["GET"])
# @exception_handler
def search_authors():
    try:
        # Create a list to hold the results
        authors_list = []

        # Query database by name of the author
        if request.args.get('published_name'):
            authors_list = db.session.query(Author).filter_by(published_name=request.args.get('published_name'))
        # Query database by collaboration, if True or False
        elif request.args.get('collaboration'):
            authors_list = db.session.query(Author).filter_by(collaboration=request.args.get('collaboration'))
        # Query database by pen name, if True or False
        elif request.args.get('pen_name'):
            authors_list = db.session.query(Author).filter_by(pen_name=request.args.get('pen_name'))
        # Query database by the name of a collaborator
        elif request.args.get('collaborator_name'):
            authors_list = db.session.query(Author).filter_by(collaborator_name=request.args.get('collaborator_name'))
        elif authors_list == []:
            return abort(400, description="Missing or invalid query string.")

        # Return authors_list in JSON format
        result = authors_schema.dump(authors_list)
        return jsonify(result)
    except exc.DataError:
        return abort(400, description="Invalid parameter in query string")


# Query the authors table with author_id
@authors.route("/search/<int:id>", methods=["GET"])
@exception_handler
def search_author(id):
    # Query database by author_id
    author = db.session.query(Author).filter_by(id=id).first()
    if not author:
        return jsonify(message="Invalid query string.")

    # Return authors in JSON format
    result = author_schema.dump(author)
    return jsonify(result)


# Allow an admin user to add a new author to the author table
# Requires details for the new author in the request body
# Must include "published_name", "collaboration, collaborator_name" and "pen_name"
@authors.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_author():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add an author.")
        
        # Add the new author's details
        author = Author()
        author_fields = author_schema.load(request.json)
        author.published_name = author_fields["published_name"]
        author.collaboration = author_fields["collaboration"]
        author.collaborator_name = author_fields["collaborator_name"]
        author.pen_name = author_fields["pen_name"]

        # Commit the new author's details to the author table
        db.session.add(author)
        db.session.commit()

        return jsonify(message="You have added an author to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and all fields are inclusion.")


# Allow an admin user to change data for an entry in the author table
# Requires details of the change to a author in the request body
# Must include "published_name", "collaboration, collaborator_name" and "pen_name"
@authors.route("/update/<int:author_id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_author(author_id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)
        
        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add an author.")
        
        # Find the author by id
        author = db.session.query(Author).filter_by(id=author_id).first()
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