from app import ma
from marshmallow import fields
from app import db


class BookSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "title", "isbn", "length", "first_publication_date", "copies_published", "author_id", "publisher_id", "read", "movie", "author", "publisher") 

        load_only = ["movie", "read", "author_id", "publisher_id"]

    author = ma.Nested("AuthorSchema", only=("published_name", ))
    publisher = ma.Nested("PublisherSchema", only=("publisher_name", ))
    read = fields.List(fields.Nested("ReadSchema", only=["rating"]))
    movie = fields.List(fields.Nested("ReadSchema", only=["rating"]))
    first_publication_date = fields.DateTime(format='%d-%m-%Y')

#add backref to read table and use python control to get average of the books

book_schema = BookSchema()
books_schema = BookSchema(many=True)