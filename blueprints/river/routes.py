from resources import db
from sqlalchemy import and_
from blueprints.river.model import River
from flask import Blueprint, request, jsonify
from blueprints.river.schema import river_schema, rivers_schema

river_blueprint = Blueprint('river_blueprint', __name__, url_prefix="/river")


@river_blueprint.route('/', methods=['POST'])
def add_river():
    name = request.json['name']
    image_url = request.json['image_url']
    length_in_km = request.json['length_in_km']
    basin_area_in_sq_km = request.json['basin_area_in_sq_km']

    new_river = River(name, image_url, length_in_km, basin_area_in_sq_km)

    db.session.add(new_river)
    db.session.commit()

    return river_schema.jsonify(new_river)


@river_blueprint.route('/<river_id>', methods=['PUT'])
def update_river(river_id):
    river = River.query.get_or_404(river_id)

    name = request.json['name']
    image_url = request.json['image_url']
    length_in_km = request.json['length_in_km']
    basin_area_in_sq_km = request.json['basin_area_in_sq_km']

    river.name = name
    river.image_url = image_url
    river.length_in_km = length_in_km
    river.basin_area_in_sq_km = basin_area_in_sq_km

    db.session.commit()

    return river_schema.jsonify(river)


@river_blueprint.route('/<river_id>', methods=['GET'])
def get_river(river_id):
    river = River.query.get_or_404(river_id)
    return river_schema.jsonify(river)


@river_blueprint.route('/', methods=['GET'])
def get_rivers():
    if request.args:
        filters = [getattr(River, attribute) == value for attribute, value in request.args.items()]
        rivers = River.query.filter(and_(*filters)).all()
    else:
        rivers = River.query.all()
    result = rivers_schema.dump(rivers)
    return jsonify(result)


@river_blueprint.route('/<river_id>', methods=['DELETE'])
def delete_river(river_id):
    river = River.query.get_or_404(river_id)

    db.session.delete(river)
    db.session.commit()

    return river_schema.jsonify(river)
