from typing import Any, Tuple

from flask_restx import Resource
from ...models.computer import Computer
from flask import request, abort
from .dto import ComputerDto, ComputerSchema
from ... import db
from ..brand.controller import BrandFilter
from ..graphics.controller import GraphicsFilter

api = ComputerDto.api
computer = ComputerDto.computer
schema = ComputerSchema


class ComputerFilter:
	def all(self, model, brand_id, graphics_id, processor_id, memory_id, harddrive_id, screen_id, wifi, bluetooth,
	        weight, cdrom, usb2, usb3, usbC, hdmi, vga, prix, prix_promo, ean):
		return Computer.query.filter_by(
			model=model,
			brand_id=brand_id,
			graphics_id=graphics_id,
			processor_id=processor_id,
			memory_id=memory_id,
			harddrive_id=harddrive_id,
			screen_id=screen_id,
			wifi=wifi,
			bluetooth=bluetooth,
			weight=weight,
			cdrom=cdrom,
			usb2=usb2,
			usb3=usb3,
			usbC=usbC,
			hdmi=hdmi,
			vga=vga,
			prix=prix,
			prix_promo=prix_promo,
			ean=ean
		).first()

	def id(self):
		return Computer.query.filter_by(id=self).first()

	def model(self):
		return Computer.query.filter_by(model=self).first()

	def brand(self):
		return Computer.query.filter_by(brand_id=self).first()

	def graphics(self):
		return Computer.query.filter_by(graphics_id=self)

	def ean(self):
		return Computer.query.filter_by(ean=self).first()


@api.route('/')
class ComputerGet(Resource):
	def get(self):
		return ComputerSchema(many=True).dump(Computer.query.all())

	@api.expect(computer)
	def post(self):
		rq_json = request.get_json()
		model, brand_id, graphics_id = rq_json["model"], rq_json["brand_id"], rq_json["graphics_id"]
		processor_id, memory_id, harddrive_id = rq_json["processor_id"], rq_json["memory_id"], rq_json["harddrive_id"]
		screen_id, wifi, bluetooth = rq_json["screen_id"], rq_json["wifi"], rq_json["bluetooth"]
		weight, cdrom, usb2, usb3, ean = rq_json["weight"], rq_json["cdrom"], rq_json["usb2"], rq_json["usb3"], rq_json[
			"ean"]
		usbC, hdmi, vga, prix, prix_promo = rq_json["usbC"], rq_json["hdmi"], rq_json["vga"], rq_json["prix"], rq_json[
			"prix_promo"]

		if ComputerFilter.all(model, brand_id, graphics_id, processor_id, memory_id, harddrive_id,
		                      screen_id, wifi, bluetooth, weight, cdrom, usb2, usb3, usbC,
		                      hdmi, vga, prix, prix_promo, ean):
			return abort(400, "Cet ordinateur existe déjà")
		new_computer = Computer(
			model=model, brand_id=brand_id, graphics_id=graphics_id, processor_id=processor_id,
			memory_id=memory_id, harddrive_id=harddrive_id, screen_id=screen_id, wifi=wifi,
			bluetooth=bluetooth, weight=weight, cdrom=cdrom, usb2=usb2, usb3=usb3, usbC=usbC,
			hdmi=hdmi, vga=vga, prix=prix, prix_promo=prix_promo, ean=ean
		)
		db.session.add(new_computer)
		db.session.commit()
		return api.payload, 201


@api.route('/id=<int:id>')
class ComputerId(Resource):
	def get(self, id):
		if ComputerFilter.id(id):
			return ComputerSchema().dumps(ComputerFilter.id(id))
		return abort(404, "Ce pc n'existe pas")

	@api.expect(computer)
	def put(self, id):
		rq_json = request.get_json()
		computer = ComputerFilter.id(id)
		if computer:
			computer.model = rq_json['model']
			computer.brand_id = rq_json['brand_id']
			computer.graphics_id = rq_json['graphics_id']
			computer.processor_id = rq_json['processor_id']
			computer.memory_id = rq_json['memory_id']
			computer.harddrive_id = rq_json['harddrive_id']
			computer.screen_id = rq_json['screen_id']
			computer.wifi = rq_json['wifi']
			computer.bluetooth = rq_json['bluetooth']
			computer.weight = rq_json['weight']
			computer.cdrom = rq_json['cdrom']
			computer.usb2 = rq_json['usb2']
			computer.usb3 = rq_json['usb3']
			computer.usbC = rq_json['usbC']
			computer.hdmi = rq_json['hdmi']
			computer.vga = rq_json['vga']
			computer.prix = rq_json['prix']
			computer.prix_promo = rq_json['prix_promo']
			computer.ean = rq_json['ean']
			db.session.commit()
			return api.payload, 201
		return abort(404, "Ce pc n'existe pas")

	def delete(self, id):
		if ComputerFilter.id(id):
			db.session.delete(ComputerFilter.id(id))
			db.session.commit()
			return api.payload, 201
		return abort(404, "Ce pc n'existe pas")


@api.route('/model=<string:model>')
class ComputerModel(Resource):
	def get(self, model):
		if ComputerFilter.model(model):
			return ComputerSchema().dumps(ComputerFilter.model(model))
		return abort(404, "Ce modèle n'existe pas")


@api.route('/brand=<string:brand>')
class ComputerBrand(Resource):
	def get(self, brand):
		if BrandFilter.all(brand):
			return ComputerSchema().dumps(ComputerFilter.brand(BrandFilter.all(brand).id))
		return abort(404, "Cette marque n'existe pas")


@api.route('/graphics=<string:graphics>')
class ComputerGraphics(Resource):
	def get(self, graphics):
		if GraphicsFilter.brand(graphics).first():
			cg_brand = GraphicsFilter.brand(graphics).first()
			return ComputerSchema(many=True).dumps(ComputerFilter.graphics(cg_brand.id).all())
		elif GraphicsFilter.model(graphics):
			cg_model = GraphicsFilter.model(graphics)
			return ComputerSchema(many=True).dumps(ComputerFilter.graphics(cg_model.id).all())
		return abort(404, "Cette carte graphique n'existe pas")


@api.route('/ean=<int:ean>')
class ComputerEan(Resource):
	def get(self, ean):
		if ComputerFilter.ean(ean):
			return ComputerSchema().dumps(ComputerFilter.ean(ean))
		return abort(404, "Cette pc n'existe pas")
