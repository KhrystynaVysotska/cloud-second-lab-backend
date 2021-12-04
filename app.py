import json
import threading
from flask import Flask
from flask_cors import CORS

from blueprints.measurement.model import Measurement
from resources import db, ma
from google.cloud import pubsub_v1
from blueprints.river.routes import river_blueprint
from blueprints.locality.routes import locality_blueprint
from blueprints.measurement.routes import measurement_blueprint
from blueprints.float_sensor.routes import float_sensor_blueprint
from blueprints.measurement_point.routes import measurement_point_blueprint
from settings import PROJECT_ID, PUBSUB_SUBSCRIPTION


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


@app.route("/")
def default():
    return "RIVER WATER LEVEL APP BACKEND"


def callback(message):
    payload = json.loads(bytes.decode(message.data))

    timestamp = payload['timestamp']
    float_sensor_id = int(payload['id'].replace('device-', ''))
    water_level_in_metres = round(float(payload['river_water_level']), 2)

    new_measurement = Measurement(timestamp, water_level_in_metres, float_sensor_id)

    with app.app_context():
        db.session.add(new_measurement)
        db.session.commit()

    message.ack()


def pub_sub_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, PUBSUB_SUBSCRIPTION)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    def run_job():
        with subscriber:
            try:
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()

    thread = threading.Thread(target=run_job)
    thread.start()


with app.app_context():
    pub_sub_subscribe()


if __name__ == "__main__":
    app.run(debug=True)