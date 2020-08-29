from . import Column, Integer, String, Model, relationship
from .. import db


class Memory(Model):
	db.__tablename__ = "Memory"
	db.__mapper__ = {'column_prefix':'Memory'}
	id = Column(Integer, primary_key = True)
	memory_capacity = Column(Integer, unique = False, nullable = False)
	memory_type = Column(String(10), unique = False, nullable = False)
	memory_frequency = Column(String, unique = False, nullable = False)
	computers = relationship('Computer', backref = "memory")

	def __repr__(self):
		f"Memory('{self.id}','{self.memory_capacity}','{self.memory_type}','{self.memory_frequency}')"