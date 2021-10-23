from resources import db
from sqlalchemy import and_
from blueprints.measurement_point.model import MeasurementPoint
from blueprints.measurement_point.schema import measurement_point_schema, measurement_points_schema
from flask import Blueprint, request, jsonify

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
