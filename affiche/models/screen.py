from . import Column, String, Integer, Model, relationship
from .. import db


class Screen(Model):
	db.__tablename__ = "screen"
	db.__mapper__ = {'column_prefix': 'screen'}
	id = Column(Integer, primary_key = True)
	screen_size = Column(Integer, unique = False, nullable = False)
	screen_resolution = Column(String(10), unique = False, nullable = False)
	screen_type = Column(String(10), unique = False, nullable = False)
	computers = relationship('Computer', backref="screen")

	def __repr__(self):
		return f"Screen('{self.id}', '{self.screen_size}', '{self.screen_resolution}', '{self.screen_type}')"