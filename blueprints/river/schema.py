from resources import ma


class RiverSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'image_url', 'length_in_km', 'basin_area_in_sq_km')


river_schema = RiverSchema()
rivers_schema = RiverSchema(many=True)