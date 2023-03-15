from app import ma
from marshmallow import fields


class MovieSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "title", "release_date", "length", "box_office_ranking", "director", "production", "book", "director_id", "production_company_id",  "book_id") 

        # Define fields to load only
        load_only = ["book_id", "director_id", "production_company_id", ]

    # Define fields to expose for nested schema
    director = ma.Nested("DirectorSchema", only=("director_name", ))
    production = ma.Nested("ProductionSchema", only=("name", ))
    book = ma.Nested("BookSchema", only=("title", ))
    # Format date
    release_date = fields.DateTime(format='%d-%m-%Y')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)