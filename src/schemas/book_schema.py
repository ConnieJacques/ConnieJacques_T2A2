from app import ma
from marshmallow import fields


class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "title", "isbn", "length", "first_publication_date", "copies_published", "author_id", "publisher_id", "author", "publisher") 

        # Define fields to load only
        load_only = ["author_id", "publisher_id"]

    # # Define fields to expose for nested schema
    author = ma.Nested("AuthorSchema", only=["published_name"])
    publisher = ma.Nested("PublisherSchema", only=["publisher_name"])
    # Format date
    first_publication_date = fields.DateTime(format='%d-%m-%Y')


book_schema = BookSchema()
books_schema = BookSchema(many=True)