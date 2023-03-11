from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import select
from models.users import User
from schemas.user_schema import user_schema, users_schema
from datetime import timedelta
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from werkzeug.exceptions import HTTPException, UnprocessableEntity


# Define blueprint 
auth = Blueprint('auth', __name__, url_prefix="/auth")


# Register a new general user
# Requires first_name, surname, email and password fields in request body
@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

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

        # Set JWT expiry time-frame
        expiry = timedelta(days=1)
        # Create JWT and assign to the user
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        jsonify({"user": user.email, "token": access_token})
        # return auth_register(200, "You have successfully registered.")
        return jsonify(message="You have successfully registered."), 200


# User login
# Required user's email and password in the request body
@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)
    # Verify user by email address
    user = User.query.filter_by(email=user_fields["email"]).first()

    # Return an error if the user's details are incorrect or the user does not exist in the database
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Account not found. Incorrect username and/or password.")

    #create a variable that sets an expiry date
    expiry = timedelta(days=1)
    #create the access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    # return the user email and the access token
    return jsonify({"user": user.first_name, "token": access_token})


# Return a user from the database
# Query by email address
@auth.route("/user/<string:email>", methods=["GET"])
@jwt_required()
def get_user(email):
    user = User.query.filter_by(email=email).first()

    # Return an error if the user is not found because they are not registered or their email address has been entered incorrectly
    if not user:
        return abort(400, description="User not found. Please check your email address is correct. If you have not registered, please do so and try again.")
    
    # Return the user's user_id, first_name and surname
    result = user_schema.dump(user)
    return jsonify(result)


# Update user information for an existing user.
# Requires user's updated details in the request body
# Must include first_name, surname, email and password
@auth.route("/user/update", methods=["PUT"])
@jwt_required()
def auth_update():
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)

    # If user is not already registered return an error message
    if not user:
        return abort(400, description="User not found. You are not registered.")
    else:
        # Update the user's details
        user_fields = user_schema.load(request.json)
        user.first_name = user_fields["first_name"]
        user.surname = user_fields["surname"]
        user.email = user_fields["email"]
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

        # Commit the new user's details to the user table
        db.session.commit()

        return jsonify(message="You have successfully updated your information."), 200


# Change admin status of an existing user
# Requires the new admin status in the request body
@auth.route("/register/admin", methods=["PUT"])
@jwt_required()
def auth_admin_register():
    # Verify the user by getting their JWT identity querying the database with the id
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)

    # If user is already not registered return an error message
    if not user:
        return abort(400, description="Account not found. Please register and login as a general user before trying again.")
    else:
        # If the user is registered, change their admin status
        user_fields = user_schema.load(request.json)
        user.admin = user_fields["admin"]

        # Commit the new user's details to the user table
        db.session.commit()

        return jsonify(message="Your admin privileges have changed."), 200


# Delete a user from the database
@auth.route("/user/unregister", methods=["DELETE"])
@jwt_required()
def auth_delete():
    # Verify user by their JWT identify and find the user in the database
    verify_user = get_jwt_identity()
    user = User.query.get(verify_user)
    
    # Return an error if the user is not found because they are not registered or their email address has been entered incorrectly
    if not user:
        return abort(401, description="User's details could not be verified. You are authorized to remove this user.")
    # Allow admin user to delete any user
    elif (user.admin == True):
        db.session.delete(user)
        db.session.commit()
    else:
        # Delete the user from the database. Cascading delete on User model will ensure all entries made to the database by the user will also be removed
        db.session.delete(user)
        db.session.commit()

    return jsonify(message="User registration has been removed."), 200