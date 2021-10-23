from resources import db


class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(45), nullable=False)
    region = db.Column(db.String(45))
    settlement = db.Column(db.String(45), nullable=False)
    image_url = db.Column(db.String(128))

    measurement_points = db.relationship("MeasurementPoint", backref="locality", cascade="all, delete")

    def __init__(self, country, region, settlement, image_url):
        self.country = country
        self.region = region
        self.settlement = settlement
        self.image_url = image_url
