from . import Column, Model, Integer, String, relationship
from .. import db


class Brand(Model):
    db.__tablename__ = "Brand"
    db.__mapper__ = {'column_prefix': 'Brand'}
    id = Column(Integer, primary_key=True)
    brandname = Column(String(30), unique=True, nullable=False)
    computers = relationship('Computer', backref='brandname')

    def __repr__(self):
        return f"Brand('{self.id}', '{self.brandname}')"
