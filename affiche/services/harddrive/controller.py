from flask_restx import Resource
from ...models.harddrive import Harddrive
from flask import request, jsonify, abort
from ... import db
from .dto import HddDto, HddSchema


api = HddDto.api
hdd = HddDto.hardrive


class HddFilter():
	def all(type, capacity):
		return Harddrive.query.filter_by(hdd_type=type, hdd_capacity=capacity).first()

	def id(id):
		return Harddrive.query.filter_by(id=id).first()

	def type(type):
		return Harddrive.query.filter_by(hdd_type=type)

	def capacity(capacity):
		return Harddrive.query.filter_by(hdd_capacity=capacity)


@api.route('/')
class HddGet(Resource):
	@api.doc(model=hdd)
	def get(self):
		return {"hdd":HddSchema(many=True).dump(Harddrive.query.all())}

	@api.expect(hdd)
	@api.doc('Ajouter un nouveau disque dur')
	def post(self):
		hdd_type = request.get_json()["hdd_type"]
		hdd_capacity = request.get_json()["hdd_capacity"]
		if HddFilter.all(hdd_type, hdd_capacity):
			return abort(400, "Ce disque existe déjà")
		db.session.add(Harddrive(hdd_type=hdd_type, hdd_capacity= hdd_capacity))
		db.session.commit()
		return api.payload, 201


@api.route('/type=<string:type>')
class HddSelectType(Resource):
	def get(self, type):
		if HddFilter.type(type).first():
			return HddSchema(many=True).dump(HddFilter.type(type).all())
		return abort(404, "Ce type de disque n'existe pas")


@api.route('/capacity=<int:capacity>')
class HddSelectCapacity(Resource):
	def get(self, capacity):
		if HddFilter.capacity(capacity).first():
			return HddSchema(many=True).dump(HddFilter.capacity(capacity).all())
		return abort(404, "Pas de disque de cette capacité")


@api.route('/id=<int:id>')
class HddSelectId(Resource):
	def get(self, id):
		if HddFilter.id(id):
			return HddSchema().dumps(HddFilter.id(id))
		return abort(404, "Ce disque n'existe pas")

	@api.expect(hdd)
	def put(self, id):
		rq_json = request.get_json()
		if HddFilter.id(id):
			HddFilter.id(id).hdd_type = rq_json["hdd_type"]
			HddFilter.id(id).hdd_capacity = rq_json["hdd_capacity"]
			db.session.commit()
			return api.payload, 201
		return abort(404, "Ce disque n'existe pas")

	def delete(self, id):
		if HddFilter.id(id):
			db.session.delete(HddFilter.id(id))
			db.session.commit()
			return jsonify('Disque dur supprimer')
		return jsonify("Ce disque n'existe pas")
