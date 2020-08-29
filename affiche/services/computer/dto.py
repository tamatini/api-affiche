from flask_restx import Namespace, fields
from ... import ma
from ...models.computer import Computer
from ..brand.dto import BrandSchema
from ..graphics.dto import GraphicsSchema
from ..processor.dto import ProcSchema
from ..memory.dto import MemorySchema
from ..harddrive.dto import HddSchema
from ..screen.dto import ScreenSchema


BrandSchema = BrandSchema()
Computer = Computer()


class ComputerSchema(ma.SQLAlchemySchema):
	class Meta:
		model = Computer
		include_fk = True

	id = ma.auto_field()
	model = ma.auto_field()
	brandname = ma.Nested(BrandSchema)
	graphicscard = ma.Nested(GraphicsSchema)
	processor = ma.Nested(ProcSchema)
	memory = ma.Nested(MemorySchema)
	harddrive = ma.Nested(HddSchema)
	screen = ma.Nested(ScreenSchema)
	wifi = ma.auto_field()
	bluetooth = ma.auto_field()
	weight = ma.auto_field()
	cdrom = ma.auto_field()
	usb2 = ma.auto_field()
	usb3 = ma.auto_field()
	usbC = ma.auto_field()
	hdmi = ma.auto_field()
	vga = ma.auto_field()
	prix = ma.auto_field()
	prix_promo = ma.auto_field()
	ean = ma.auto_field()


class ComputerDto:
	api = Namespace('computer', description="Computer")
	computer = api.model(
		'computer',
		{
			'model': fields.String(required=True, description="Modèle du pc"),
			'brand_id': fields.Integer(required=True, description="Marque du pc"),
			'graphics_id': fields.Integer(required=True, description="Carte Graphique"),
			'processor_id': fields.Integer(required=True, description="Processeur"),
			'memory_id': fields.Integer(required=True, description="Mémoire"),
			'harddrive_id': fields.Integer(required=True, description="Harddrive"),
			'screen_id': fields.Integer(required=True, description="Ecran"),
			'wifi': fields.String(required=True, description="Possède wifi"),
			'bluetooth': fields.String(required=True, description="Possède bluetooth"),
			'weight': fields.Integer(required=True, description="Poid de l'ordinateur"),
			'cdrom': fields.String(required=True, description="Possède cdrom"),
			'usb2': fields.Integer(required=True, description="Nombre d'usb2.0"),
			'usb3': fields.Integer(required=True, description="Nombre d'usb3.0"),
			'usbC': fields.Integer(required=True, description="Nombre d'usb-C"),
			'hdmi': fields.String(required=True, description="Possède le hdmi"),
			'vga': fields.String(required=True, description="Possède le vga"),
			'prix': fields.Integer(required=True, description="Prix de l'ordinateur"),
			'prix_promo': fields.Integer(required=True, description="Prix promo de l'ordinateur"),
			'ean': fields.Integer(required=True, description="Code barre de l'ordinateur")
		}
	)