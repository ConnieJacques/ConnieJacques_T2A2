from app import ma


class PublisherSchema(ma.Schema):
    class Meta:
        ordered = True
        # Define the fields to expose
        fields = ("id", "publisher_name")


publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True)