from resources import db
from sqlalchemy import and_
from blueprints.locality.model import Locality
from flask import Blueprint, request, jsonify
from blueprints.locality.schema import locality_schema, localities_schema

locality_blueprint = Blueprint('locality_blueprint', __name__, url_prefix="/locality")


@locality_blueprint.route('/', methods=['POST'])
def add_locality():
    country = request.json['country']
    region = request.json['region']
    settlement = request.json['settlement']
    image_url = request.json['image_url']

    new_locality = Locality(country, region, settlement, image_url)

    db.session.add(new_locality)
    db.session.commit()

    return locality_schema.jsonify(new_locality)


@locality_blueprint.route('/<locality_id>', methods=['PUT'])
def update_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)

    country = request.json['country']
    region = request.json['region']
    settlement = request.json['settlement']
    image_url = request.json['image_url']

    locality.country = country
    locality.region = region
    locality.settlement = settlement
    locality.image_url = image_url

    db.session.commit()

    return locality_schema.jsonify(locality)


@locality_blueprint.route('/<locality_id>', methods=['GET'])
def get_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)
    return locality_schema.jsonify(locality)


@locality_blueprint.route('/', methods=['GET'])
def get_localities():
    if request.args:
        filters = [getattr(Locality, attribute) == value for attribute, value in request.args.items()]
        localities = Locality.query.filter(and_(*filters)).all()
    else:
        localities = Locality.query.all()
    result = localities_schema.dump(localities)
    return jsonify(result)


@locality_blueprint.route('/<locality_id>', methods=['DELETE'])
def delete_locality(locality_id):
    locality = Locality.query.get_or_404(locality_id)

    db.session.delete(locality)
    db.session.commit()

    return locality_schema.jsonify(locality)
