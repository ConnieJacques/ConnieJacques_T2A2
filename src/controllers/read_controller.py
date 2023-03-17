from flask import Blueprint, jsonify, request, abort
from app import db
from marshmallow import exceptions
from models.users import User
from models.read import Read
from schemas.read_schema import read_schema, reads_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from helper import exception_handler


# Define blueprint 
read = Blueprint('read', __name__, url_prefix="/read")


# Query the read table to return all and only the user's entries 
@read.route("/<int:user_id>", methods=["GET"])
@exception_handler
@jwt_required()
def read_id(user_id):
    # Verify the user by getting their JWT identity and querying the database with the id
    verify_user = get_jwt_identity()
    user = db.session.query(User).get(verify_user)

    # If user is not already registered return an error message
    if not user:
        return abort(400, description="User not found. Please login.")
    
    # Return reviews matching the user id
    if user.id == user_id:
        results = db.session.query(Read).filter(Read.user_id == user_id).all()
        # Return a message if there are no reviews
        if len(results) == 0:
            return jsonify(message="You have not reviewed any books.")
        result = reads_schema.dump(results)
        return jsonify(result)
    # Return error message if the user id does not match the user id for the review
    elif user.id != user_id:
        return abort(403, "Invalid user id. You are not authorized to access this information.")


# Query read table with book id to see the average rating 
@read.route("/rating/<int:book_id>", methods=["GET"])
@exception_handler
def read_ratings(book_id):
    try:
        # Query read table to book id and get the average rating
        average = db.session.query(Read).filter(Read.book_id == book_id).with_entities(db.func.avg(Read.rating)).scalar()
        
        # Return a message if book id does not match an entry in the database
        if not average:
            return jsonify(message="No rating available for this book id.")
        
        average = round(average, 2)

        # Return rating in a message
        return jsonify(message=f"The average rating of this book is: {average}"), 200
        # Return an error message if the book id does not match an entry in the database
    except TypeError:
        return jsonify(message="No rating available for this book id.")


# Allow a user to add a rating
@read.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_read():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        verify_user = get_jwt_identity()
        user = db.session.query(User).get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")

        # Get the details of the new book view
        read = Read()
        read_fields = read_schema.load(request.json)
        read.rating = read_fields["rating"]
        read.book_id = read_fields["book_id"]
        read.user_id = user.id

        # Commit the review to the read table
        db.session.add(read)
        db.session.commit()

        return jsonify(message="You have added a review."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")


# Update the rating for an entry in the read table only if the same user is attempting to make the change
@read.route("/update/<int:review_id>", methods=["PUT"])
@exception_handler
@jwt_required()
def update_read(review_id):
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        verify_user = get_jwt_identity()
        user = db.session.query(User).get(verify_user)

        if not user:
            return abort(400, description="User not found. Please login.")
        
        # Get the requested review from the database
        read = db.session.query(Read).filter(Read.id == review_id).first()

        if not read:
            return abort(404, description="A review with this id does not exist.")

        # Return an error if the user does not own the review
        if read.user_id != user.id:
            return abort(403, description="You are not authorized to change this record.")
            
        # Update the rating
        read_fields = read_schema.load(request.json)
        read.rating = read_fields["rating"]

        # Commit the update to the database
        db.session.add(read)
        db.session.commit()

        return jsonify(message="You have successfully updated your rating for this book."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")
    

# Allow a user to delete an individual entry from the read table
@read.route("/delete/<int:read_id>", methods=["DELETE"])
@exception_handler
@jwt_required()
def delete_read(read_id):
    # Verify the user by getting their JWT identity and querying the database with the id
    verify_user = get_jwt_identity()
    user = db.session.query(User).get(verify_user)
    
    if not user:
        return abort(400, description="User not found. Please login.")
    
    # Get the requested review from the database
    read = db.session.query(Read).filter(Read.user_id == user.id).first()

    if not read:
        return abort(403, description="You are not authorized to change this record.")
    
    read = db.session.query(Read).filter(Read.id == read_id).first()

    if not read:
        return abort(400, description="Review could not be located. Incorrect or invalid id.")

    # Delete the review from the database
    db.session.delete(read)
    db.session.commit()

    return jsonify(message="You have successfully deleted your review for this book."), 200