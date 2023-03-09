from app import ma
from marshmallow import fields


class ProductionSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "name")

production_schema = ProductionSchema()
productions_schema = ProductionSchema(many=True)