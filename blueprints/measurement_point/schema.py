from resources import ma
from blueprints.river.schema import RiverSchema
from blueprints.locality.schema import LocalitySchema
from blueprints.float_sensor.schema import FloatSensorSchema


class MeasurementPointSchema(ma.Schema):
    class Meta:
        fields = ('id', 'zero_point_in_metres', 'max_water_level_in_metres', 'river', 'locality', 'float_sensors')

    river = ma.Nested(RiverSchema)
    locality = ma.Nested(LocalitySchema)
    float_sensors = ma.Nested(FloatSensorSchema, many=True)


measurement_point_schema = MeasurementPointSchema()
measurement_points_schema = MeasurementPointSchema(many=True)
