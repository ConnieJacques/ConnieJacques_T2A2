from app import ma
from marshmallow import fields
from marshmallow.validate import Range


class WatchedSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "user_id", "movie_id", "user", "movie", "rating")

        # Define fields to load only
        load_only = ["user_id", "movie_id"]
        
    # Define ratings between 1 - 10
    rating = ma.validate=Range(min=1, max=10)
    # Define fields to expose for nested schema
    user = ma.Nested("UserSchema", only=["first_name", "surname"])
    movie = fields.Nested("MovieSchema", only=["title"])


watch_schema = WatchedSchema()
watched_schema = WatchedSchema(many=True)