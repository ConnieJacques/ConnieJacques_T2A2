from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import desc
from marshmallow import exceptions
from models.users import User
from models.watched import Watched
from schemas.watched_schema import watched_schema, watch_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import exception_handler


# Define blueprint 
watched = Blueprint('watched', __name__, url_prefix="/watched")


# Query watched table to return all and only the user's entries 
@watched.route("/<int:user_id>", methods=["GET"])
@exception_handler
@jwt_required()
def watched_id(user_id):
    # Verify the user by getting their JWT identity and querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)

    # If user is not already registered return an error message
    if not user:
        return abort(400, description="User not found. Please login.")
    
    # Return results if JWT identity matches the user id for the results
    if user.id == user_id:
        results = db.session.query(Watched).filter(Watched.user_id == user_id).all()
        # Return a message if there are no reviews
        if len(results) == 0:
            return jsonify(message="You have not reviewed any books.")
        result = watched_schema.dump(results)
        return jsonify(result)
    # Return error message if the user id does not match the user id for the review
    elif user.id != user_id:
        return abort(403, "Invalid user id. You are not authorized to access this information.")


# Query read table with movie id to see the average rating 
@watched.route("/rating/<int:movie_id>", methods=["GET"])
@exception_handler
def read_ratings(movie_id):
    try:
        # Query read table to book id and get the average rating
        average = db.session.query(Watched).filter(Watched.movie_id == movie_id).with_entities(db.func.avg(Watched.rating)).scalar()
        
        # Return a message if movie id does not match an entry in the database
        if not average:
            return jsonify(message="No rating available for this movie id.")
        
        average = round(average, 2)

        # Return rating in a message
        return jsonify(message=f"The average rating of this movie is: {average}"), 200
        # Return an error message if the book id does not match an entry in the database
    except TypeError:
        return jsonify(message="No rating available for this movie id.")


# Allow a user to add a rating
@watched.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_watched():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        verify_user = get_jwt_identity()
        user = db.session.query(User).get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")

        # Get the details of the new movie review
        watched = Watched()
        watched_fields = watch_schema.load(request.json)
        watched.rating = watched_fields["rating"]
        watched.movie_id = watched_fields["movie_id"]
        watched.user_id = user.id

        # Commit the review to the watched table
        db.session.add(watched)
        db.session.commit()

        return jsonify(message="You have added a review."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")
    


# Update the rating for an entry in the watched table only if the same user is attempting to make the change
@watched.route("/update/<int:id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_watched(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        if not user:
            return abort(400, description="User not found. Please login.")
        
        # Get the requested review from the database
        watched = db.session.query(Watched).filter(Watched.id == id).first()

        if not watched:
            return abort(404, description="A review with this id does not exist.")

        # Return an error if the user does not own the review
        if watched.user_id != user.id:
            return abort(403, description="You are not authorized to change this record.")
            
         # Update the rating
        watched_fields = watch_schema.load(request.json)
        watched.rating = watched_fields["rating"]

        # Commit the update to the database
        db.session.add(watched)
        db.session.commit()

        return jsonify(message="You have successfully updated your rating for this movie."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")


# Allow a user to delete an individual entry from the watched table
@watched.route("/delete/<int:watched_id>", methods=["DELETE"])
@exception_handler
@jwt_required()
def delete_watched(watched_id):
    # Verify the user by getting their JWT identity and querying the database with the id
    verify_user = get_jwt_identity()
    user = db.session.query(User).get(verify_user)
    
    if not user:
        return abort(400, description="User not found. Please login.")
    
    # Get the requested review from the database
    watched = db.session.query(Watched).filter(Watched.user_id == user.id).first()

    if not watched:
        return abort(403, description="You are not authorized to change this record.")
    
    watched = db.session.query(Watched).filter(Watched.id == watched_id).first()

    if not watched:
        return abort(400, description="Review could not be located. Incorrect or invalid id.")

    # Delete the review from the database
    db.session.delete(watched)
    db.session.commit()

    return jsonify(message="You have successfully deleted your review for this movie."), 200