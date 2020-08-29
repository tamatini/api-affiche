from flask_restx import Namespace, fields
from ... import ma
from ...models.graphics import Graphics
from ...models.computer import Computer


graphics = Graphics()
computer = Computer()


class GraphicsSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = graphics


class GraphicsDto:
	api = Namespace('graphics', description="Carte Graphique")
	graphics = api.model(
		'graphics',
		{
			'graphics_brand': fields.String(required=True, description="Marque de la carte graphique"),
			'graphics_model': fields.String(required=True, description="Modèle de la carte graphique"),
			'graphics_memory': fields.Integer(required=True, description="Capacité de mémoire")
		}
	)