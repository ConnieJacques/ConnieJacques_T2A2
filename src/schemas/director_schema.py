from app import ma


class DirectorSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "director_name")


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)