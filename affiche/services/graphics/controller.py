from flask_restx import Resource
from ...models.graphics import Graphics
from flask import request, jsonify, abort
from ... import db
from .dto import GraphicsDto, GraphicsSchema


api = GraphicsDto.api
graphics = GraphicsDto.graphics


class GraphicsFilter():
	def all(brand, model, memory):
		return Graphics.query.filter_by(graphics_brand=brand, graphics_model=model, graphics_memory=memory).first()

	def id(id):
		return Graphics.query.filter_by(id=id).first()

	def brand(brand):
		return Graphics.query.filter_by(graphics_brand=brand)

	def model(model):
		return Graphics.query.filter_by(graphics_model=model).first()

	def memory(memory):
		return Graphics.query.filter_by(graphcis_memory=memory)


@api.route("/")
class GraphicsGet(Resource):
	@api.doc(model=graphics)
	def get(self):
		return GraphicsSchema(many=True).dump(Graphics.query.all())

	@api.marshal_with(graphics)
	@api.expect(graphics)
	@api.doc("Ajouter une nouvelle carte graphique")
	def post(self):
		rq_json = request.get_json()
		brand = rq_json['graphics_brand']
		model = rq_json['graphics_model']
		memory = rq_json['graphics_memory']
		if GraphicsFilter.all(brand, model, memory):
			return abort(400, "Cette carte graphique existe déjà")
		db.session.add(Graphics(graphics_brand=brand, graphics_model=model, graphics_memory=memory))
		db.session.commit()
		return api.payload, 201

@api.route('/brand=<string:brand>')
class GraphicsGetByBrand(Resource):
	@api.doc('Liste des cartes graphique par marque')
	def get(self, brand):
		if GraphicsFilter.brand(brand).first():
			return GraphicsSchema(many=True).dump(GraphicsFilter.brand(brand).all())
		return abort(404, "Pas de carte graphique de cette marque")


@api.route('/model=<string:model>')
class GraphicsGetByModel(Resource):
	@api.doc(model=graphics)
	def get(self, model):
		if GraphicsFilter.model(model):
			return GraphicsSchema().dump(GraphicsFilter.model(model))
		return abort(404, "Cette carte graphique n'existe pas")


@api.route('/id=<int:id>')
class GraphicGetById(Resource):
	@api.doc(model=graphics)
	def get(self, id):
		if GraphicsFilter.id(id):
			return GraphicsSchema().dump(GraphicsFilter.id(id))
		return abort(404, "Cette carte graphique n'existe pas")

	@api.expect(graphics)
	def put(self, id):
		if GraphicsFilter.id(id):
			GraphicsFilter.id(id).graphics_model=request.get_json()['graphics_model']
			GraphicsFilter.id(id).graphics_brand=request.get_json()['graphics_brand']
			db.session.commit()
			return api.payload, 201
		return abort(404, "Cette carte graphique n'existe pas")

	def delete(self, id):
		if GraphicsFilter.id(id):
			db.session.delete(GraphicsFilter.id(id))
			db.session.commit()
			return api.payload, 201
		return abort(404, "Cette carte graphique n'existe pas")
