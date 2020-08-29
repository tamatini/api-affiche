from . import Column, Integer, String, Model
from .. import db


class Computer(Model):
	db.__tablename__ = "Computer"
	db.__mapper__ = {'column_prefix': 'Computer'}
	id = Column(Integer, primary_key = True)
	model = Column(String(50), unique = True, nullable = False)
	brand_id = Column(Integer, db.ForeignKey('brand.id'))
	graphics_id = Column(Integer, db.ForeignKey('graphics.id'))
	processor_id = Column(Integer, db.ForeignKey('processor.id'))
	memory_id = Column(Integer, db.ForeignKey('memory.id'))
	harddrive_id = Column(Integer, db.ForeignKey('harddrive.id'))
	screen_id = Column(Integer, db.ForeignKey('screen.id'))
	wifi = Column(String(10), unique = False, nullable = False)
	bluetooth = Column(String(10), unique = False, nullable = False)
	weight = Column(Integer, unique = False, nullable = False)
	cdrom = Column(String(10), unique = False, nullable = False)
	usb2 = Column(Integer, unique = False, nullable = False)
	usb3 = Column(Integer, unique = False, nullable = False)
	usbC = Column(Integer, unique = False, nullable = False)
	hdmi = Column(String(5), unique = False, nullable = False)
	vga = Column(String(5), unique = False, nullable = False)
	prix = Column(Integer, unique = False, nullable = False)
	prix_promo = Column(Integer, unique = False, nullable = False)
	ean = Column(Integer, unique = True, nullable = False)

	def __repr__(self):
		f"Computer(" \
		f"'{self.id}','{self.model}','{self.wifi}','{self.bluetooth}'," \
		f"'{self.weight}','{self.cdrom}','{self.usb2}','{self.usb3}'," \
		f"'{self.usbC}','{self.hdmi}','{self.vga}','{self.prix}'," \
		f"'{self.prix_promo}','{self.ean}')"