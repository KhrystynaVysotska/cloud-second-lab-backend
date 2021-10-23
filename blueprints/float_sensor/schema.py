from resources import ma


class FloatSensorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'geo_point', 'measurement_point_id')


float_sensor_schema = FloatSensorSchema()
float_sensors_schema = FloatSensorSchema(many=True)
