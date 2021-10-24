from resources import db


class River(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    image_url = db.Column(db.String(128))
    length_in_km = db.Column(db.Numeric, nullable=False)
    basin_area_in_sq_km = db.Column(db.Numeric, nullable=False)

    measurement_points = db.relationship("MeasurementPoint", backref="river", cascade="all, delete")

    def __init__(self, name, image_url, length_in_km, basin_area_in_sq_km):
        self.name = name
        self.image_url = image_url
        self.length_in_km = length_in_km
        self.basin_area_in_sq_km = basin_area_in_sq_km
