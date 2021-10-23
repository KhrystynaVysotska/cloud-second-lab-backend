from resources import db


class MeasurementPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    river_id = db.Column(db.Integer, db.ForeignKey('river.id'), nullable=False)
    locality_id = db.Column(db.Integer, db.ForeignKey('locality.id'), nullable=False)
    zero_point_in_metres = db.Column(db.Numeric, nullable=False)
    max_water_level_in_metres = db.Column(db.Numeric, nullable=False)
    float_sensors = db.relationship("FloatSensor", backref="measurement_point", cascade="all, delete")

    def __init__(self, river_id, locality_id, zero_point_in_metres, max_water_level_in_metres):
        self.river_id = river_id
        self.locality_id = locality_id
        self.zero_point_in_metres = zero_point_in_metres
        self.max_water_level_in_metres = max_water_level_in_metres
