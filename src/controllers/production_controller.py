from flask import Blueprint, jsonify, request, abort
from app import db
from marshmallow import exceptions
from models.movies import ProductionCompany
from schemas.production_company_schema import production_schema, productions_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from helper import exception_handler


# Define blueprint 
production = Blueprint('production', __name__, url_prefix="/production")


# Query database to get all the production companies from the production_company table. 
# Public access - no authentication required
@production.route("/", methods=["GET"])
@exception_handler
def get_all_production_companies():
    production = db.session.query(ProductionCompany).all()
    result = productions_schema.dump(production)
    return jsonify(result)


# Query the production_company table with a query string to get a production company by name
@production.route("/search/name/<string:name>", methods=["GET"])
@exception_handler
def search_production_name(name):
    # Query database by the name of the production company
    production = db.session.query(ProductionCompany).filter_by(name=name).first()

    # Return an error if name is invalid
    if not production:
        return abort(400, description="Production company not found.")

    # Return a production company in JSON format
    result = production_schema.dump(production)
    return jsonify(result)


# Query the production_company table with production_company_id to return the company
@production.route("/search/<int:id>", methods=["GET"])
@exception_handler
def search_production_id(id):
    # Query database by production_id
    production = db.session.query(ProductionCompany).filter_by(id=id).first()

    # Return error message if the id passed is invalid
    if not production:
        return abort(400, description="Production company not found.")

    # Return a production company in JSON format
    result = production_schema.dump(production)
    return jsonify(result)


# Allow an admin user to add a new production company to the production_company table
# Requires details for the new production company in the request body
# Must include production company "name"
@production.route("/add", methods=["POST"])
@exception_handler
@jwt_required()
def add_production_company():
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a production company.")
        else:
            # Add the new production company's details
            production = ProductionCompany()
            production_fields = production_schema.load(request.json)
            production.name = production_fields["name"]

            # Commit the new production companies details to the production company table
            db.session.add(production)
            db.session.commit()

            return jsonify(message="You have added a production company to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.") 
    

# Allow an admin user to change data for an entry in the production company table
# Requires details of the change in the request body
# Must include production company "name"
@production.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_production_company(id):
    try:
        # Verify the user by getting their JWT identity and querying the database with the id
        validate_user = get_jwt_identity()
        user = db.session.query(User).get(validate_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a production company.")
        
        # Find the production company by id
        production = db.session.query(ProductionCompany).filter_by(id=id).first()
        if not production:
            return abort(400, description= "Production company could not be located in the database.")
        
        # Add the new production companies details
        production_fields = production_schema.load(request.json)
        production.name = production_fields["name"]

        # Commit the updated details to the publisher table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes and that all fields are included.")