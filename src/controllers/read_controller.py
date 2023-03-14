from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.users import User
from models.read import Read
from schemas.read_schema import read_schema, reads_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


# Define blueprint 
read = Blueprint('read', __name__, url_prefix="/read")


# Query read table to return all and only the user's entries 
@read.route("/<int:id>", methods=["GET"])
@jwt_required()
def read_id(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.id == id:
            results = db.session.query(Read).filter(Read.user_id == id).all()
            result = reads_schema.dump(results)
            return jsonify(result)
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    

@read.route("/add", methods=["POST"])
@jwt_required()
def add_read():
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)

    # If user is not already registered return an error message
    if not user:
        return abort(400, description="User not found. Please login.")
    else:
        # Add the new movie's details
        read = Read()
        read_fields = read_schema.load(request.json)
        read.rating = read_fields["rating"]
        read.book_id = read_fields["book_id"]
        read.user_id = user.id


        # Commit the new movie's details to the movie table
        db.session.add(read)
        db.session.commit()

        return jsonify(message="You have added a movie to the table."), 200
    


# Update the rating for an entry in the read table only if the same user is attempting to make the change
@read.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_read(id):
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)
    if not user:
        return abort(400, description="User not found. Please login.")
    
    read = db.session.query(Read).filter(Read.id == id).first()

    if read.user_id != user.id:
        return abort(403, description="You are not authorized to change this record.")
        
    # Add the new movie's details
    read_fields = read_schema.load(request.json)
    read.rating = read_fields["rating"]
    read.book_id = read.book_id
    read.user_id = read.user_id

    # Commit the new movie's details to the movie table
    db.session.add(read)
    db.session.commit()

    return jsonify(message="You have successfully updated your rating for this book."), 200


# Allow a user to delete an individual entry from the read table
@read.route("/delete/<int:user_id>/<int:read_id>", methods=["DELETE"])
@jwt_required()
def delete_read(user_id, read_id):
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)
    if not user:
        return abort(400, description="User not found. Please login.")
    
    read = db.session.query(Read).filter(Read.id == user_id).first()

    if read.user_id != user.id:
        return abort(403, description="You are not authorized to change this record.")
    
    read = db.session.query(Read).filter(Read.id == read_id).first()

    # Commit the updated details to the book table
    db.session.delete(read)
    db.session.commit()

    return jsonify(message="You have successfully deleted your review for this book."), 200