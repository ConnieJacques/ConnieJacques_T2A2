from app import ma


class AuthorSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "published_name", "pen_name", "collaboration", "collaborator_name")


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)   