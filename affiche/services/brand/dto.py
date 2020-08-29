from flask_restx import Namespace, fields
from ...models.brand import Brand
from ...models.computer import Computer
from ... import ma


brand = Brand()
computer = Computer()


class BrandSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = brand


class BrandDto:
    api = Namespace('brand', description="Marque")
    brand = api.model(
        'brand',
        {
            'brandname': fields.String(required=True, description="Marque de l'appareil")
        }
    )