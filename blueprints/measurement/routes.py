import json
import base64
import flask
from resources import db
from sqlalchemy import and_
from flask import Blueprint, request, jsonify
from blueprints.measurement.model import Measurement
from blueprints.measurement.schema import measurement_schema, measurements_schema
from settings import PUBSUB_VERIFICATION_TOKEN
from sse.MessageAnnouncer import MessageAnnouncer
from sse.utils import format_sse

measurement_blueprint = Blueprint('measurement_blueprint', __name__, url_prefix="/measurement")

announcer = MessageAnnouncer()


@measurement_blueprint.route('/', methods=['POST'])
def add_measurement():
    timestamp = request.json['timestamp']
    float_sensor_id = request.json['float_sensor_id']
    water_level_in_metres = request.json['water_level_in_metres']

    new_measurement = Measurement(timestamp, water_level_in_metres, float_sensor_id)

    db.session.add(new_measurement)
    db.session.commit()

    return measurement_schema.jsonify(new_measurement)


@measurement_blueprint.route('/<measurement_id>', methods=['PUT'])
def update_measurement(measurement_id):
    measurement = Measurement.query.get_or_404(measurement_id)

    timestamp = request.json['timestamp']
    float_sensor_id = request.json['float_sensor_id']
    water_level_in_metres = request.json['water_level_in_metres']

    measurement.timestamp = timestamp
    measurement.float_sensor_id = float_sensor_id
    measurement.water_level_in_metres = water_level_in_metres

    db.session.commit()

    return measurement_schema.jsonify(measurement)


@measurement_blueprint.route('/<measurement_id>', methods=['GET'])
def get_measurement(measurement_id):
    measurement = Measurement.query.get_or_404(measurement_id)
    return measurement_schema.jsonify(measurement)


@measurement_blueprint.route('/', methods=['GET'])
def get_measurements():
    if request.args:
        filters = [getattr(Measurement, attribute) == value for attribute, value in request.args.items()]
        measurements = Measurement.query.filter(and_(*filters)).all()
    else:
        measurements = Measurement.query.all()
    result = measurements_schema.dump(measurements)
    return jsonify(result)


@measurement_blueprint.route('/<measurement_id>', methods=['DELETE'])
def delete_measurement(measurement_id):
    measurement = Measurement.query.get_or_404(measurement_id)
    measurement_json_data = measurement_schema.jsonify(measurement)

    db.session.delete(measurement)
    db.session.commit()

    return measurement_json_data


@measurement_blueprint.route('/message', methods=['POST'])
def get_measurement_message():
    if request.args.get('token', '') != PUBSUB_VERIFICATION_TOKEN:
        return 'Invalid request', 400

    envelope = json.loads(request.data)
    payload = json.loads(base64.b64decode(envelope['message']['data']))

    timestamp = payload['timestamp']
    float_sensor_id = payload['id'].replace('device-', '')
    water_level_in_metres = round(float(payload['river_water_level']), 2)

    new_measurement = Measurement(timestamp, water_level_in_metres, float_sensor_id)

    db.session.add(new_measurement)
    db.session.commit()

    msg = format_sse(data=measurement_schema.dumps(new_measurement, default=str), event=float_sensor_id)
    announcer.announce(msg=msg)

    return measurement_schema.jsonify(new_measurement)


@measurement_blueprint.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()
        while True:
            msg = messages.get()
            print(msg)
            yield msg

    return flask.Response(stream(), status=200, mimetype='text/event-stream')
