from resources import db
from custom_types.Point import Point


class FloatSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    geo_point = db.Column(Point, nullable=False)
    measurement_point_id = db.Column(db.Integer, db.ForeignKey('measurement_point.id'), nullable=False)
    measurements = db.relationship("Measurement", backref="float_sensor", cascade="all, delete")

    def __init__(self, geo_point, measurement_point_id):
        self.geo_point = geo_point
        self.measurement_point_id = measurement_point_id
