from resources import ma
from blueprints.float_sensor.schema import FloatSensorSchema


class MeasurementSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'water_level_in_metres', 'float_sensor_id', 'float_sensor')

    float_sensor = ma.Nested(FloatSensorSchema)


measurement_schema = MeasurementSchema()
measurements_schema = MeasurementSchema(many=True)
