from flask import Blueprint


# Define blueprint 
home = Blueprint('home', __name__, url_prefix="/")

# Greet the user and direct them to the README for directions on how to use the api
@home.route("/", methods=["GET"])
def go_home():
    return "Welcome to the Stephen King API. Please refer to the README for detailed information about of all available endpoints."