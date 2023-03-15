from app import ma


class AuthorSchema(ma.Schema):
    class Meta:
        # Define the fields to expose
        fields = ("id", "published_name", "collaboration", "pen_name", "collaborator_name")


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)   