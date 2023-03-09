from flask import Blueprint, jsonify, request, abort
from app import db
from sqlalchemy import select
from models.users import User
from schemas.user_schema import user_schema, users_schema
from datetime import timedelta
from app import bcrypt
from flask_jwt_extended import create_access_token


# Define blueprint 
home = Blueprint('home', __name__, url_prefix="/")

@home.route("/")
def go_home():
    return "Welcome to the Stephen King API. Please refer to the README for detailed information about of all available endpoints."