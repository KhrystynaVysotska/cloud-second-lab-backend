from resources import db
from sqlalchemy import and_
from flask import Blueprint, request, jsonify
from blueprints.float_sensor.model import FloatSensor
from blueprints.float_sensor.schema import float_sensor_schema, float_sensors_schema

float_sensor_blueprint = Blueprint('float_sensor_blueprint', __name__, url_prefix="/float_sensor")


@float_sensor_blueprint.route('/', methods=['POST'])
def add_float_sensor():
    geo_point = request.json['geo_point']
    measurement_point_id = request.json['measurement_point_id']

    new_float_sensor = FloatSensor(geo_point, measurement_point_id)

    db.session.add(new_float_sensor)
    db.session.commit()

    return float_sensor_schema.jsonify(new_float_sensor)


@float_sensor_blueprint.route('/<float_sensor_id>', methods=['PUT'])
def update_float_sensor(float_sensor_id):
    float_sensor = FloatSensor.query.get_or_404(float_sensor_id)

    geo_point = request.json['geo_point']
    measurement_point_id = request.json['measurement_point_id']

    float_sensor.geo_point = geo_point
    float_sensor.measurement_point_id = measurement_point_id

    db.session.commit()

    return float_sensor_schema.jsonify(float_sensor)


@float_sensor_blueprint.route('/<float_sensor_id>', methods=['GET'])
def get_float_sensor(float_sensor_id):
    float_sensor = FloatSensor.query.get_or_404(float_sensor_id)
    return float_sensor_schema.jsonify(float_sensor)


@float_sensor_blueprint.route('/', methods=['GET'])
def get_float_sensors():
    if request.args:
        filters = [getattr(FloatSensor, attribute) == value for attribute, value in request.args.items()]
        float_sensors = FloatSensor.query.filter(and_(*filters)).all()
    else:
        float_sensors = FloatSensor.query.all()
    result = float_sensors_schema.dump(float_sensors)
    return jsonify(result)


@float_sensor_blueprint.route('/<float_sensor_id>', methods=['DELETE'])
def delete_float_sensor(float_sensor_id):
    float_sensor = FloatSensor.query.get_or_404(float_sensor_id)
    float_sensor_json_data = float_sensor_schema.jsonify(float_sensor)

    db.session.delete(float_sensor)
    db.session.commit()

    return float_sensor_json_data
