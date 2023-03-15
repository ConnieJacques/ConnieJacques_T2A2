from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    # Create Flask object
    app = Flask(__name__)

    # Configure Flask
    app.config.from_object("config.app_config")

    # Create SQLAlchemy, Marshmallow, JWT and Bcrypt objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import commands
    from commands import db_commands
    app.register_blueprint(db_commands)

    # Import controllers
    from controllers import registerable_controllers
    # Register blueprints
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app