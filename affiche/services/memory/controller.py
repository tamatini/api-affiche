from flask_restx import Resource
from ...models.memory import Memory
from flask import request, jsonify, abort
from ... import db
from .dto import MemoryDto, MemorySchema


api = MemoryDto.api
memory = MemoryDto.memory

class MemoryFilter():
	def all(capacity, type, frequency):
		return Memory.query.filter_by(
			memory_capacity= capacity,
			memory_type=type,
			memory_frequency=frequency
		).first()

	def id(id):
		return Memory.query.filter_by(id=id).first()

	def capacity(capacity):
		return Memory.query.filter_by(memory_capacity=capacity).first()

	def type(type):
		return Memory.query.filter_by(memory_type=type).first()

	def frequency(frequency):
		return Memory.query.filter_by(memory_frequency=frequency).first()


@api.route('/')
class MemoryGet(Resource):
	@api.doc("Récupère la liste de toutes les mémoires vives")
	def get(self):
		return MemorySchema(many=True).dumps(Memory.query.all())

	@api.expect(memory)
	def post(self):
		req_json = request.get_json()
		capacity = req_json['memory_capacity']
		type = req_json['memory_type']
		frequency = req_json['memory_frequency']
		if MemoryFilter.all(capacity, type, frequency):
			return abort(400, "Cette memoire existe déjà")
		db.session.add(Memory(memory_capacity=capacity, memory_type=type, memory_frequency=frequency))
		db.session.commit()
		return api.payload, 201


@api.route('/id=<int:id>')
class MemoryGetById(Resource):
	@api.doc("Récupère les mémoires vives par Id")
	def get(self, id):
		if MemoryFilter.id(id):
			return MemorySchema().dump(MemoryFilter.id(id))
		return abort(404, "Cette mémoire n'existe pas")

	def delete(self, id):
		if MemoryFilter.id(id):
			db.session.delete(MemoryFilter.id(id))
			db.session.commit()
			return jsonify("Cette mémoire à été supprimer")
		return abort(404, "Cette mémoire n'exite pas")

	@api.expect(memory)
	def put(self, id):
		req_json = request.get_json()
		if MemoryFilter.id(id):
			MemoryFilter.id(id).memory_capacity = req_json['memory_capacity']
			MemoryFilter.id(id).memory_type = req_json['memory_type']
			MemoryFilter.id(id).memory_frequency = req_json['memory_frequency']
			db.session.commit()
			return api.payload, 201
		return abort(404, "Cette mémoire n'existe pas")


@api.route('/capacity=<string:capacity>')
class MemoryGetByCapacity(Resource):
	def get(self, capacity):
		if MemoryFilter.capacity(capacity):
			return MemorySchema().dump(MemoryFilter.capacity(capacity))
		return abort(404, "Cette mémoire n'existe pas")


@api.route('/type=<string:type>')
class MemoryGetByType(Resource):
	def get(self, type):
		if MemoryFilter.type(type):
			return MemorySchema().dump(MemoryFilter.type(type))
		return abort(404, "Ce type n'existe pas")


@api.route('/frequency=<string:frequency>')
class MemoryGetByFrequency(Resource):
	def get(self, frequency):
		if MemoryFilter.frequency(frequency):
			return MemorySchema().dump(MemoryFilter.frequency(frequency))
		return abort(404, "Cette fréquence n'existe pas")