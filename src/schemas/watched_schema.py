from app import ma
from marshmallow import fields
from marshmallow.validate import Range


class WatchedSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "user_id", "movie_id", "rating")
        
    rating = ma.validate=Range(min=1, max=10)
    user = fields.Nested("UserSchema", only="id.first_name.surname")
    movie = fields.List(fields.Nested("MovieSchema"))

watch_schema = WatchedSchema()
watched_schema = WatchedSchema(many=True)