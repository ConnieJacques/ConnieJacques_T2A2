from app import ma
from marshmallow.validate import Length
from marshmallow import fields

class UserSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ['id', 'first_name', 'surname', 'email', 'password', 'admin', 'read', 'watched']

        load_only = ['email', 'password', 'admin']

    #Set the password's length to exactly 8 character long
    password = ma.String(validate=Length(equal=8))
    read = fields.List(fields.Nested("ReadSchema", exclude=("user")))
    watched = fields.List(fields.Nested("WatchedSchema", exclude=("user",)))

user_schema = UserSchema()
users_schema = UserSchema(many=True)