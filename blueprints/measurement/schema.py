from resources import ma


class MeasurementSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'water_level_in_metres', 'float_sensor_id')


measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)
