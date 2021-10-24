from resources import db
from sqlalchemy import and_, func, desc
from flask import Blueprint, request, jsonify
from blueprints.measurement.model import Measurement
from blueprints.float_sensor.model import FloatSensor
from blueprints.measurement.schema import measurement_schema
from blueprints.float_sensor.schema import float_sensor_schema
from blueprints.measurement_point.model import MeasurementPoint
from blueprints.measurement_point.schema import measurement_point_schema, measurement_points_schema, \
    measurement_point_schema_exclude_float_sensors

measurement_point_blueprint = Blueprint('measurement_point_blueprint', __name__, url_prefix="/measurement_point")


@measurement_point_blueprint.route('/', methods=['POST'])
def add_measurement_point():
    river_id = request.json['river_id']
    locality_id = request.json['locality_id']
    zero_point_in_metres = request.json['zero_point_in_metres']
    max_water_level_in_metres = request.json['max_water_level_in_metres']

    new_measurement_point = MeasurementPoint(river_id, locality_id, zero_point_in_metres, max_water_level_in_metres)

    db.session.add(new_measurement_point)
    db.session.commit()

    return measurement_point_schema.jsonify(new_measurement_point)


@measurement_point_blueprint.route('/<measurement_point_id>', methods=['PUT'])
def update_measurement_point(measurement_point_id):
    measurement_point = MeasurementPoint.query.get_or_404(measurement_point_id)

    river_id = request.json['river_id']
    locality_id = request.json['locality_id']
    zero_point_in_metres = request.json['zero_point_in_metres']
    max_water_level_in_metres = request.json['max_water_level_in_metres']

    measurement_point.river_id = river_id
    measurement_point.locality_id = locality_id
    measurement_point.zero_point_in_metres = zero_point_in_metres
    measurement_point.max_water_level_in_metres = max_water_level_in_metres

    db.session.commit()

    return measurement_point_schema.jsonify(measurement_point)


@measurement_point_blueprint.route('/<measurement_point_id>', methods=['GET'])
def get_measurement_point(measurement_point_id):
    measurement_point = MeasurementPoint.query.get_or_404(measurement_point_id)
    return measurement_point_schema.jsonify(measurement_point)


@measurement_point_blueprint.route('/', methods=['GET'])
def get_measurement_points():
    if request.args:
        filters = [getattr(MeasurementPoint, attribute) == value for attribute, value in request.args.items()]
        measurement_points = MeasurementPoint.query.filter(and_(*filters)).all()
    else:
        measurement_points = MeasurementPoint.query.all()
    result = measurement_points_schema.dump(measurement_points)
    return jsonify(result)


@measurement_point_blueprint.route('/<measurement_point_id>', methods=['DELETE'])
def delete_measurement_point(measurement_point_id):
    measurement_point = MeasurementPoint.query.get_or_404(measurement_point_id)
    measurement_point_json_data = measurement_point_schema.jsonify(measurement_point)

    db.session.delete(measurement_point)
    db.session.commit()

    return measurement_point_json_data


@measurement_point_blueprint.route('/latest', methods=['GET'])
def get_latest_measurement_data():
    row_number_column = func.row_number().over(partition_by=Measurement.float_sensor_id,
                                               order_by=desc(Measurement.timestamp)).label('row_number')

    query = db.session.query(MeasurementPoint, FloatSensor, Measurement) \
        .join(MeasurementPoint.float_sensors) \
        .join(FloatSensor.measurements)

    query = query.add_column(row_number_column)

    result = query.from_self().filter(row_number_column == 1).all()

    result_list = []
    for measurement_point, float_sensor, measurement, row_number in result:
        result_object = {
            'measurement_point': measurement_point_schema_exclude_float_sensors.dump(measurement_point),
            'float_sensor': float_sensor_schema.dump(float_sensor),
            'measurement': measurement_schema.dump(measurement)}
        result_list.append(result_object)

    return jsonify(result_list)
