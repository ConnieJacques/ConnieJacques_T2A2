from flask import Blueprint, jsonify, request, abort
from app import db
from marshmallow import exceptions
from models.users import User
from schemas.user_schema import user_schema, users_schema
from datetime import timedelta
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import exc
from helper import exception_handler, verify_user


# Define blueprint 
auth = Blueprint('auth', __name__, url_prefix="/auth")


# Register a new general user
# Requires first_name, surname, email and password fields in request body
@auth.route("/register", methods=["POST"])
@exception_handler
def auth_register():
    try:
        # Get the user's email address from the request body and verify they are not already registered
        user_fields = user_schema.load(request.json)
        user = db.session.query(User).filter_by(email=user_fields["email"]).first()

        # If user is already registered return an error message
        if user:
            return abort(400, description="You are already registered.")
        else:
            # If user is not already registered, add the user
            user = User()
            user.first_name  = user_fields["first_name"]
            user.surname = user_fields["surname"]
            user.email = user_fields["email"]
            user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
            
            # Commit the new user's details to the user table
            db.session.add(user)
            db.session.commit()
            return jsonify(message="You have successfully registered.")
    # Return an error message if the user's password in the request body is unacceptable
    except exceptions.ValidationError:
        return abort(400, description="Password must be exactly 8 characters long. Request body field requires a string.")


# User login
# Required user's email and password in the request body
@auth.route("/login", methods=["POST"])
@exception_handler
def auth_login():
    # Get the user's email address from the request body and find a match in the database
    user_fields = user_schema.load(request.json)
    user = db.session.query(User).filter_by(email=user_fields["email"]).first()

    # Return an error if the user's details are incorrect or the user does not exist in the database
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(400, description="Account not found. Incorrect username and/or password.")

    # Set JWT expiry time-frame
    expiry = timedelta(days=1)
    # Create JWT and assign to the user
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # Return the user's email address and the access token
    return jsonify({"user": user.first_name, "token": access_token})


# Allow admin users to view all user
@auth.route("/user/all", methods=["GET"])
@exception_handler
@jwt_required()
def admin_get_users():
    # Verify the user by getting their JWT identity querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)

    # If the user's id from the token does not match any record in the database, return an error
    if not user:
        return abort(401, description="User not found.")
    
    # Get all users from the database
    users = db.session.query(User).all()

    # If user is an admin return all users
    if user.admin == True:
        result = users_schema.dump(users)
        return jsonify(result)
    # If not, return an error
    else:
        return abort(403, description="You are not authorized to access this information.")


# Return a user from the database
# Query by email address
@auth.route("/user/<string:email>", methods=["GET"])
@exception_handler
@jwt_required()
def get_user(email):
    # Verify the user by getting their JWT identity querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)

    # If the user's id from the token does not match any record in the database, return an error
    if not user:
        return abort(401, description="User not found.")
    
    # Use the email address provided in the URL to query the database for a match
    user_email = db.session.query(User).filter(User.email == email).first()

    # If email provided does not match any record in the database, return an error
    if not user_email:
        return abort(400, description="User not found.")
    
    # If a record is found but the user id from the JWT token does not match the user id on the record, return an error
    if (user_email.id != user.id):
        return abort(403, description="You are not authorized to access this information.")
    
    # Return the user's user_id, first_name and surname
    result = user_schema.dump(user)
    return jsonify(result)



# Update user information for an existing user
# Requires user's updated details in the request body
# Must include first_name, surname, email and password
@auth.route("/user/update", methods=["PUT"])
@exception_handler
@jwt_required()
def auth_update():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If the user's id from the token does not match any record in the database, return an error
        if not user:
            return abort(400, description="User not found.")
        
        # Update the user's details
        user_fields = user_schema.load(request.json)
        user.first_name = user_fields["first_name"]
        user.surname = user_fields["surname"]
        user.email = user_fields["email"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

        # Commit the user's new details to the user table
        db.session.commit()

        return jsonify(message="You have successfully updated your information.")
    except exceptions.ValidationError:
        return abort(400, description="Password must be exactly 8 characters long. Request body field requires a string.")


# Change admin status of an existing user
# Requires the new admin status in the request body
@auth.route("/register/admin/<int:id>", methods=["PUT"])
@exception_handler
@jwt_required()
def auth_admin_register(id):
    # Verify the user by getting their JWT identity querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)

    # If the user's id from the token does not match any record in the database, return an error
    if not user:
        return abort(400, description="User not found.")
    elif user.admin != True:
        return abort(403, description="You are not authorized to access to make this change.")
    
    user_to_admin = db.session.query(User).filter(User.id == id).first()
    
    # If the user is registered, change their admin status
    user_fields = user_schema.load(request.json)
    user_to_admin.admin = user_fields["admin"]

    # Commit the new user's details to the user table
    db.session.commit()

    return jsonify(message="Your admin privileges have changed."), 200


# Delete a user from the database
@auth.route("/user/unregister/<string:email>", methods=["DELETE"])
@exception_handler
@jwt_required()
def auth_delete(email):
    # Verify the user by getting their JWT identity querying the database with the id
    validate_user = get_jwt_identity()
    user = db.session.query(User).get(validate_user)

    # If the user's id from the token does not match any record in the database, return an error
    if not user:
        return abort(401, description="User not found.")

    # Use the email address provided in the URL to query the database for a match
    user_email = db.session.query(User).filter(User.email == email).first()

    # If email provided does not match any record in the database, return an error
    if not user_email:
        return abort(400, description="User not found.")
    
    # If a record is found but the user id from the JWT token does not match the user id on the record, return an error
    if (user_email.id != user.id):
        return abort(403, description="You are not authorized to access this information.")


    # Delete the user from the database
    # Cascading delete on User model will ensure all entries made to the database by the user will also be removed
    db.session.delete(user)
    db.session.commit()

    return jsonify(message="User registration has been removed."), 200