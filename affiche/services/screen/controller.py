from flask_restx import Resource, abort
from flask import request, jsonify
from .dto import ScreenDto, ScreenSchema
from ...models.screen import Screen
from ... import db


api = ScreenDto.api
screen = ScreenDto.screen

class Screen_filter():
	def all(size, resolution, type):
		return Screen.query.filter_by(
			screen_size=size,
			screen_resolution=resolution,
			screen_type=type
		).first()

	def id(id):
		return Screen.query.filter_by(id=id).first()

	def size(size):
		return Screen.query.filter_by(screen_size=size)

	def resolution(resolution):
		return Screen.query.filter_by(screen_resolution=resolution)

	def type(type):
		return Screen.query.filter_by(screen_type=type)


@api.route('/')
class ScreenGet(Resource):
	@api.doc(model=screen)
	def get(self):
		return {"screen": ScreenSchema(many=True).dump(Screen.query.all())}

	@api.expect(screen)
	def post(self):
		rq_json = request.get_json()
		screen_size = rq_json["screen_size"]
		screen_resolution = rq_json["screen_resolution"]
		screen_type = rq_json["screen_type"]
		if Screen_filter.all(screen_size, screen_resolution, screen_type):
			return abort(400, "Cette écran existe déjà")
		db.session.add(Screen(screen_size=screen_size, screen_resolution=screen_resolution, screen_type=screen_type))
		db.session.commit()
		return api.payload, 201


@api.route('/id=<int:id>')
class ScreenGetById(Resource):
	@api.doc("Récupère les écrans par ID")
	def get(self, id):
		if Screen_filter.id(id):
			return ScreenSchema().dumps(Screen_filter.id(id))
		return abort(404, "Cet écran n'existe pas")

	def delete(self, id):
		if Screen_filter.id(id):
			db.session.delete(Screen_filter.id(id))
			db.session.commit()
			return jsonify("L'écran à été supprimer")
		return abort(404, "Cet écran n'existe pas")

	@api.expect(screen)
	def put(self, id):
		rq_json = request.get_json()
		if Screen_filter.id(id):
			Screen_filter.id(id).screen_size = rq_json['screen_size']
			Screen_filter.id(id).screen_resolution = rq_json['screen_resolution']
			Screen_filter.id(id).screen_type = rq_json['screen_type']
			db.session.commit()
			return api.payload, 201
		return abort(404, "Cet écran n'existe pas")


@api.route('/size=<string:size>')
class ScreenGetBySize(Resource):
	@api.doc("Récupère les écrans par taille")
	def get(self, size):
		if Screen_filter.size(size).first():
			return ScreenSchema(many=True).dumps(Screen_filter.size(size))
		return abort(404, "Cette taille n'existe pas")


@api.route('/reso=<string:resolution>')
class ScreenGetByResolution(Resource):
	@api.doc("Récupère les écrans par résolution")
	def get(self, resolution):
		if Screen_filter.resolution(resolution).first():
			return ScreenSchema(many=True).dumps(Screen_filter.resolution(resolution))
		return abort(404, "Cette résolution n'existe pas")


@api.route('/type=<string:type>')
class ScreenGetByType(Resource):
	@api.doc("Récupère les écrans par type")
	def get(self, type):
		if Screen_filter.type(type).first():
			return ScreenSchema(many=True).dumps(Screen_filter.type(type))
		return abort(404, "Ce type n'existe pas")


