from app import ma
from marshmallow import fields


class DirectorSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "director_name")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)