from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.users import User
from models.watched import Watched
from schemas.watched_schema import watched_schema, watch_schema
from flask_jwt_extended import jwt_required, get_jwt_identity


# Define blueprint 
watched = Blueprint('watched', __name__, url_prefix="/watched")


# Query watched table to return all and only the user's entries 
@watched.route("/<int:id>", methods=["GET"])
@jwt_required()
def watched_id(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.id == id:
            results = db.session.query(Watched).filter(Watched.user_id == id).all()
            result = watched_schema.dump(results)
            return jsonify(result)
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    

@watched.route("/add", methods=["POST"])
@jwt_required()
def add_watched():
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)

    # If user is not already registered return an error message
    if not user:
        return abort(400, description="User not found. Please login.")
    else:
        # Add the new movie's details
        watched = Watched()
        watched_fields = watch_schema.load(request.json)
        watched.rating = watched_fields["rating"]
        watched.movie_id = watched_fields["movie_id"]
        watched.user_id = user.id


        # Commit the new movie's details to the movie table
        db.session.add(watched)
        db.session.commit()

        return jsonify(message="You have added a movie to the table."), 200
    


# Update the rating for an entry in the watched table only if the same user is attempting to make the change
@watched.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_watched(id):
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)
    if not user:
        return abort(400, description="User not found. Please login.")
    
    watched = db.session.query(Watched).filter(Watched.id == id).first()

    if watched.user_id != user.id:
        return abort(403, description="You are not authorized to change this record.")
        
    # Add the new movie's details
    watched_fields = watch_schema.load(request.json)
    watched.rating = watched_fields["rating"]
    watched.movie_id = watched.movie_id
    watched.user_id = watched.user_id

    # Commit the new movie's details to the movie table
    db.session.add(watched)
    db.session.commit()

    return jsonify(message="You have successfully updated your rating for this book."), 200


# Allow a user to delete an individual entry from the watched table
@watched.route("/delete/<int:watched_id>", methods=["DELETE"])
@jwt_required()
def delete_watched(watched_id):
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)
    if not user:
        return abort(400, description="User not found. Please login.")
    
    watched = db.session.query(Watched).filter(Watched.user_id == user.id).first()

    if not watched:
        return abort(403, description="You are not authorized to change this record.")
    
    watched = db.session.query(Watched).filter(Watched.id == watched_id).first()

    if not watched:
        return abort(400, description="Record could not be located. Incorrect or invalid id for watch table entered.")

    # Commit the updated details to the book table
    db.session.delete(watched)
    db.session.commit()

    return jsonify(message="You have successfully deleted your review for this book."), 200