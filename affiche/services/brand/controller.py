from flask_restx import Resource
from ...models.brand import Brand
from flask import request, jsonify, abort
from ... import db
from .dto import BrandDto, BrandSchema


api = BrandDto.api
brand = BrandDto.brand


class BrandFilter:
    def all(self):
        return Brand.query.filter_by(brandname=self).first()

    def id(self):
        return Brand.query.filter_by(id=self).first()

    def brand(self):
        return Brand.query.filter_by(brandname=self)


@api.route("/")
class BrandGet(Resource):
    @api.doc(model=brand)
    def get(self):
        return {"brand": BrandSchema(many=True).dump(Brand.query.all())}

    @api.doc("Ajoute une nouvelle marque")
    @api.expect(brand)
    def post(self):
        rq_json = request.get_json()
        brandname = rq_json['brandname']
        if BrandFilter.all(brandname):
            return abort(400, 'Cette marque existe déjà')
        new_marque = Brand(brandname=rq_json["brandname"])
        db.session.add(new_marque)
        db.session.commit()
        return api.payload, 201


@api.route("/id=<int:brand_id>")
class BrandSelectById(Resource):
    @api.doc(model=brand)
    def get(self, brand_id):
        if BrandFilter.id(brand_id):
            return BrandSchema().dump(BrandFilter.id(brand_id))
        return abort(404, "Cette marque n'existe pas")

    @api.expect(brand)
    def put(self, brand_id):
        if BrandFilter.id(brand_id):
            BrandFilter.id(brand_id).brandname = request.get_json()["brandname"]
            db.session.commit()
            return api.payload, 201
        return abort(400, "Cette marque n'existe pas")

    @api.doc("Supprimer une marque")
    def delete(self, brand_id):
        if BrandFilter.id(brand_id):
            db.session.delete(BrandFilter.id(brand_id))
            db.session.commit()
            return api.payload, 201
        return abort(404, "Cette marque n'existe pas")


@api.route("/brandname=<string:brandname>")
class BrandSelectByBrand(Resource):
    @api.doc(model=brand)
    def get(self, brandname):
        if BrandFilter.brand(brandname).first():
            return BrandSchema(many=True).dump(BrandFilter.brand(brandname).all())
        return abort(404, "Cette marque n'existe pas")