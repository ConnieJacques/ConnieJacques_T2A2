from app import ma
from marshmallow import fields
from marshmallow.validate import Range


class ReadSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "user_id", "book_id", "rating")
        
    rating = ma.validate=Range(min=1, max=10)
    user = fields.Nested("UserSchema", only="id.first_name.surname")
    book = fields.List(fields.Nested("BookSchema"))

read_schema = ReadSchema()
reads_schema = ReadSchema(many=True)