from flask_restx import Namespace, fields
from ... import ma
from ...models.memory import Memory
from ...models.computer import Computer


memory = Memory()
computer = Computer()


class MemorySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = memory


class MemoryDto:
	api = Namespace('memory', description="Mémoire vive")
	memory = api.model(
		'Memory', {
			'memory_capacity': fields.String(required=True, description="Capacité de la mémoire vive"),
			'memory_type': fields.String(required=True, description="Type de mémoire vive"),
			'memory_frequency': fields.String(required=True, description="Fréquence de la mémoire vive")
		}
	)