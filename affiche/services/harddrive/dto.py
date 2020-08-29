from flask_restx import Namespace, fields
from ... import ma
from ...models.harddrive import Harddrive
from ...models.computer import Computer


harddrive = Harddrive()
computer = Computer()


class HddSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = harddrive


class HddDto:
	api = Namespace('hardrive', description="Disque dur")
	hardrive = api.model(
		'Hardrive', {
			'hdd_type': fields.String(required = True, description="Type de disque dur"),
			'hdd_capacity': fields.Integer(required = True, description="Capacité du disque dur")
		}
	)