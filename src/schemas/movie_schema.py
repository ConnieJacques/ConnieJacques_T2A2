from app import ma
from marshmallow import fields


class MovieSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "title", "release_date", "length", "box_office_ranking", "book_id", "director_id", "production_company_id", "watched") 

        load_only = ["watched"]

    director = fields.Nested("DirectorSchema", only="director_name")
    production = fields.Nested("ProductionSchema", only="name")
    book_id = fields.List(fields.Nested("BookSchema", only=("title")))

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)