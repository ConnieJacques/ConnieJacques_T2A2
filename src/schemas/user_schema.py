from app import ma
from marshmallow.validate import Length


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ["id", "first_name", "surname", "email", "password", "admin"]

        # Define fields to load only
        load_only = ["email", "password"]

    #Set the password's length to exactly 8 character's
    password = ma.String(validate=Length(equal=8))


user_schema = UserSchema()
users_schema = UserSchema(many=True)