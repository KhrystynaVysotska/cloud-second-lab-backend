from resources import db


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    water_level_in_metres = db.Column(db.Numeric, nullable=False)
    float_sensor_id = db.Column(db.Integer, db.ForeignKey('float_sensor.id'), nullable=False)

    def __init__(self, timestamp, water_level_in_metres, float_sensor_id):
        self.timestamp = timestamp
        self.water_level_in_metres = water_level_in_metres
        self.float_sensor_id = float_sensor_id
