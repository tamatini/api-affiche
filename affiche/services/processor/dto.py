from flask_restx import Namespace, fields
from ... import ma
from ...models.processor import Processor
from ...models.computer import Computer


processor = Processor()
computer = Computer()


class ProcSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = processor


class ProcDto:
	api = Namespace('processor', description='Processeur')
	processor = api.model(
		'Processor', {
			'proc_brand': fields.String(required=True, description="Marque du processeur"),
			'proc_model': fields.String(required=True, description="Modèle du processeur"),
			'proc_frequency': fields.String(required=True, description="Fréquence du processeur"),
			'proc_core': fields.Integer(required=True, description="Nombre de coeurs"),
			'proc_thread': fields.Integer(required=True, description="Nombre de threads")
		}
	)