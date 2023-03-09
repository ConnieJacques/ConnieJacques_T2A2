from app import ma
from marshmallow import fields
# from schemas.author_schema import AuthorSchema
# from schemas.publisher_schema import AuthorSchema


class BookSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "title", "isbn", "length", "first_publication_date", "copies_published", "author_id", "publisher_id", "read", "movie") 

        load_only = ["movie", "read"]

    author = ma.Nested(AuthorSchema)
    publisher = ma.Nested(PublisherSchema)
    read = fields.List(fields.Nested("ReadSchema", exclude=("read")))
    movie = fields.List(fields.Nested("ReadSchema", exclude=("movie")))
    author = fields.List(fields.Nested("AuthorSchema", exclude=("id")))

book_schema = BookSchema()
books_schema = BookSchema(many=True)