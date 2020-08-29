from flask_restx import Resource, abort
from ...models.processor import Processor
from flask import request, jsonify
from ... import db
from .dto import ProcDto, ProcSchema


api = ProcDto.api
processor = ProcDto.processor

class ProcFilter():
	def all(brand, model, frequency, core, thread):
		return Processor.query.filter_by(
			proc_brand=brand,
			proc_model=model,
			proc_frequency=frequency,
			proc_core=core,
			proc_thread=thread
		).first()

	def id(id):
		return Processor.query.filter_by(id=id).first()

	def brand(brand):
		return Processor.query.filter_by(proc_brand=brand)

	def model(model):
		return Processor.query.filter_by(proc_model=model)

	def frequency(frequency):
		return Processor.query.filter_by(proc_frequency=frequency)

	def core(core):
		return Processor.query.filter_by(proc_core=core)

	def thread(thread):
		return Processor.query.filter_by(proc_thread=thread)


@api.route('/')
class ProcessorGet(Resource):
	@api.doc("Récupère la liste de tout les processeurs")
	def get(self):
		return ProcSchema(many=True).dump(Processor.query.all())

	@api.expect(processor)
	@api.doc("Ajoute un nouveau processeur")
	def post(self):
		rq_json = request.get_json()
		brand = rq_json['proc_brand']
		model = rq_json['proc_model']
		frequency = rq_json['proc_frequency']
		core = rq_json['proc_core']
		thread = rq_json['proc_thread']
		if ProcFilter.all(brand, model, frequency, core, thread):
			return abort(400, "Ce processeur existe déjà")
		db.session.add(Processor(
			proc_brand=brand,
			proc_model=model,
			proc_frequency=frequency,
			proc_core=core,
			proc_thread=thread))
		db.session.commit()
		return api.payload, 201


@api.route('/id=<int:id>')
class ProcessorSelectById(Resource):
	@api.doc("Récupère le processor par Id")
	def get(self, id):
		if ProcFilter.id(id):
			return ProcSchema().dump(ProcFilter.id(id))
		return abort(404, "Ce processeur n'existe pas")

	@api.expect(processor)
	def put(self, id):
		req_json = request.get_json()
		if ProcFilter.id(id):
			ProcFilter.id(id).proc_brand = req_json['proc_brand']
			ProcFilter.id(id).proc_model = req_json['proc_model']
			ProcFilter.id(id).proc_frequency = req_json['proc_frequency']
			ProcFilter.id(id).proc_core = req_json['proc_core']
			ProcFilter.id(id).proc_thread = req_json['proc_thread']
			db.session.commit()
			return api.payload, 201
		return abort(404, "Ce processeur n'existe pas")

	def delete(self, id):
		if ProcFilter.id(id):
			db.session.delete(ProcFilter.id(id))
			db.session.commit()
			return jsonify("Ce processeur à été supprimer")
		return abort(404, "Ce processeur n'existe pas")


@api.route('/brand=<string:brand>')
class ProcessorGetByBrand(Resource):
	def get(self, brand):
		if ProcFilter.brand(brand).first():
			return ProcSchema(many=True).dump(ProcFilter.brand(brand))
		return abort(404, "Cette marque n'existe pas")


@api.route('/model=<string:model>')
class ProcessorGetByModel(Resource):
	def get(self, model):
		if ProcFilter.model(model).first():
			return ProcSchema(many=True).dump(ProcFilter.brand(model))
		return abort(404, "Ce model n'existe pas")


@api.route('/frequency=<int:frequency>')
class ProcessorGetByFrequency(Resource):
	def get(self, frequency):
		if ProcFilter.frequency(frequency).first():
			return ProcSchema(many=True).dump(ProcFilter.frequency(frequency))
		return abort(404, "Cette fréquence n'existe pas")


@api.route('/core=<int:core>')
class ProcessorGetByCore(Resource):
	def get(self, core):
		if ProcFilter.core(core).first():
			return ProcSchema(many=True).dump(ProcFilter.core(core))
		return abort(404, "Ce core n'existe pas")


@api.route('/thread=<int:thread>')
class ProcessorGetByThread(Resource):
	def get(self, thread):
		if ProcFilter.thread(thread).first():
			return ProcSchema(many=True).dump(ProcFilter.thread(thread))
		return abort(404, "Ce thread n'existe pas")
