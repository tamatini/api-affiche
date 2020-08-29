from flask_restx import Api
from flask import Blueprint

from .brand.controller import api as brand_ns
from .harddrive.controller import api as hdd_ns
from .screen.controller import api as screen_ns
from .graphics.controller import api as graphics_ns
from .computer.controller import api as computer_ns
from .processor.controller import api as processor_ns
from .memory.controller import api as memory_ns


api_bp = Blueprint("api", __name__)


api = Api(
    api_bp,
    title="Api affiche",
    version="1.0b",
    description="Api des affiches du rayon EPCS")


api.add_namespace(brand_ns)
api.add_namespace(hdd_ns)
api.add_namespace(screen_ns)
api.add_namespace(graphics_ns)
api.add_namespace(computer_ns)
api.add_namespace(processor_ns)
api.add_namespace(memory_ns)