from resources import db
from sqlalchemy import and_
from flask import Blueprint, request, jsonify
from blueprints.measurement.model import Measurement
from blueprints.measurement.schema import measurement_schema, measurements_schema

measurement_blueprint = Blueprint('measurement_blueprint', __name__, url_prefix="/measurement")


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
