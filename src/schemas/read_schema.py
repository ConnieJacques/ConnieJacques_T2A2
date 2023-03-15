from app import ma
from marshmallow import fields
from marshmallow.validate import Range


class ReadSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "user_id", "book_id", "user", "book", "rating")

        # Define fields to load only
        load_only = ["user_id", "book_id"]
        
    # Define ratings between 1 - 10
    rating = ma.validate=Range(min=1, max=10)
    # Define fields to expose for nested schema
    user = ma.Nested("UserSchema", only=["first_name", "surname"])
    book = fields.Nested("BookSchema", only=["title"])


read_schema = ReadSchema()
reads_schema = ReadSchema(many=True)