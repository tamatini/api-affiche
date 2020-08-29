from . import Column, Integer, String, Model, relationship
from .. import db


class Graphics(Model):
	db.__tablename__ = "Graphics"
	db.__mapper__ = {'column_prefix':'Graphics'}
	id = Column(Integer, primary_key = True)
	graphics_brand = Column(String(20), unique = False, nullable = False)
	graphics_model = Column(String(30), unique = False, nullable = False)
	graphics_memory = Column(Integer, unique = False, nullable = False)
	computers = relationship('Computer', backref='graphicscard')

	def __repr__(self):
		f"Graphics('{self.id}', '{self.graphics_brand}', '{self.graphics_model}', '{self.graphics_memory}')"
