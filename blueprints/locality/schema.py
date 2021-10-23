from resources import ma


class LocalitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'country', 'region', 'settlement', 'image_url')


locality_schema = LocalitySchema()
localities_schema = LocalitySchema(many=True)