from . import Column, Model, Integer, String, relationship
from .. import db


class Harddrive(Model):
	db.__tablename__ = "Harddrive"
	db.__mapper__ = {'column_prefix': 'Harddrive'}
	id = Column(Integer, primary_key = True)
	hdd_type = Column(String(10), nullable = False, unique = False)
	hdd_capacity = Column(Integer, nullable = False, unique = False)
	computers = relationship('Computer', backref='harddrive')

	def __repr__(self):
		return f"HardDrive('{self.id}', '{self.hdd_type}', '{self.hdd_capacity}')"