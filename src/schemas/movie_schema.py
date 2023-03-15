from app import ma
from marshmallow import fields


class MovieSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "title", "release_date", "length", "box_office_ranking", "director_id", "production_company_id",  "book_id", "watched", "book", "director", "production") 

        load_only = ["watched", "book_id", "director_id", "production_company_id", ]

    director = ma.Nested("DirectorSchema", only=("director_name", ))
    production = ma.Nested("ProductionSchema", only=("name", ))
    book = ma.Nested("BookSchema", only=("title", ))
    watched = fields.List(fields.Nested("WatchedSchema", exclude=("watched", )))
    release_date = fields.DateTime(format='%d-%m-%Y')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)