from . import Integer, String, relationship, Column, Model
from .. import db


class Processor(Model):
	db.__tablename__="Processor"
	db.__mapper__ = {'column_prefix':'Processor'}
	id = Column(Integer, primary_key = True)
	proc_brand = Column(String(10), unique = False, nullable = False)
	proc_model = Column(String(10), unique = True, nullable = False)
	proc_frequency = Column(Integer, unique = False, nullable = False)
	proc_core = Column(Integer, unique = False, nullable = False)
	proc_thread = Column(Integer, unique = False, nullable = False)
	computers = relationship('Computer', backref="proc")

	def __repr__(self):
		f"Processor('{self.id}', '{self.proc_brand}', '{self.proc_model}', '{self.proc_frequency}'," \
		f"'{self.proc_core}', '{self.proc_thread}')"