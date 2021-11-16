from flask import Flask
from flask_cors import CORS
from resources import db, ma
from blueprints.river.routes import river_blueprint
from blueprints.locality.routes import locality_blueprint
from blueprints.measurement.routes import measurement_blueprint
from blueprints.float_sensor.routes import float_sensor_blueprint
from blueprints.measurement_point.routes import measurement_point_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(river_blueprint)
app.register_blueprint(locality_blueprint)
app.register_blueprint(measurement_point_blueprint)
app.register_blueprint(float_sensor_blueprint)
app.register_blueprint(measurement_blueprint)

app.config.from_pyfile("settings.py")

db.init_app(app)
ma.init_app(app)

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
