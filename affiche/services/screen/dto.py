from flask_restx import Namespace, fields
from ...models.screen import Screen
from ...models.computer import Computer
from ... import ma

screen = Screen()
computer = Computer()


class ScreenSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = screen


class ScreenDto:
	api = Namespace('screen', description="Ecran")
	screen = api.model(
		"screen", {
			'screen_size': fields.Integer(required=True, description="Taille de l'écran"),
			'screen_resolution': fields.String(required=True, description="Résolution de l'écran"),
			'screen_type': fields.String(required=True, description="Type d'écran")
		}
	)