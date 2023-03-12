from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import exc
from marshmallow import exceptions
from models.movies import ProductionCompany
from schemas.publisher_schema import production_schema, productions_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User


# Define blueprint 
production = Blueprint('production', __name__, url_prefix="/production")


# Query database to get all the production companies from the production_company table. 
# Public access - no authentication required
@production.route("/", methods=["GET"])
def get_all_production_companies():
    try:
        production = ProductionCompany.query.all()
        result = productions_schema.dump(production)
        return jsonify(result)
    # Return an error if the database is not connected or tables have not been created or seeded.
    except exc.DatabaseError:
        return abort(404, description="PostgreSQL database connection not found.")
    except exc.NoSuchTableError:
        return abort(404, description="Please ensure the database is seeded. Run {flask db create} then {flask db seed} on the command line to create and seed tables.")


# Query the production_company table with a query string to get production company by name
@production.route("/search/name/<string:name>", methods=["GET"])
def search_production_name(name):
    try:
        # Query database by the name of the production company
        production = ProductionCompany.query.filter_by(name=name).first()

        if not production:
            return abort(400, description="Production company not found.")

        # Return production company in JSON format
        result = production_schema.dump(production)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Query the production_company table with production_company_id to return the company
@production.route("/search/<int:id>", methods=["GET"])
def search_production_id(id):
    try:
        # Query database by production_id
        production = ProductionCompany.query.filter_by(id=id).first()

        if not production:
            return abort(400, description="Production company not found.")

        # Return production company in JSON format
        result = production_schema.dump(production)
        return jsonify(result)
    # Catch errors if no results is returned or an invalid query is attempted
    except exc.NoResultFound:
        return abort(404, "No results found. Please check you are using a valid query method.")
    except exc.DataError:
        return abort(404, "No results found. Please check you are using a valid query method.")


# Allow an admin user to add a new production company to the production_company table
# Requires details for the new production company in the request body
# Must include production company "name"
@production.route("/add", methods=["POST"])
@jwt_required()
def add_production_company():
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a Publisher.")
        else:
            # Add the new production company's details
            production = ProductionCompany()
            production_fields = production_schema.load(request.json)
            production.name = production_fields["name"]

            # Commit the new publisher's details to the publisher table
            db.session.add(production)
            db.session.commit()

            return jsonify(message="You have added a production company to the table."), 200
    # Handle errors within the request body
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion.")
    # Return an error if the new entry already exists in the database
    except AssertionError:
        return abort(400, description="New entry already exist in the database.")
    

# Allow an admin user to change data for an entry in the production company table
# Requires details of the change in the request body
# Must include production company "name"
@production.route("/update/<int:id>", methods=["PUT"])
@jwt_required()
def update_production_company(id):
    try:
        # Verify the user by getting their JWT identity querying the database with the id
        verify_user = get_jwt_identity()
        user = User.query.get(verify_user)

        # If user is not already registered return an error message
        if not user:
            return abort(400, description="User not found. Please login.")
        if user.admin != True:
            return abort(403, description="You are not authorized to add a production company.")
        
        # Find the publisher by id
        production = ProductionCompany.query.filter_by(id=id).first()
        if not production:
            return abort(400, description= "Production company could not be located in the database.")
        
        # Add the new production companies details
        production_fields = production_schema.load(request.json)
        production.name = production_fields["name"]

        # Commit the updated details to the publisher table
        db.session.commit()

        return jsonify(message="You have successfully updated the database."), 200
    except exceptions.ValidationError:
        return abort(400, description="Error in request body. Please check for spelling mistakes, full data inclusion. Dates must be formatted as DD-MM-YYYY")
    except KeyError:
        return abort(400, "Information incorrect in request body. Please ensure all fields are included.")