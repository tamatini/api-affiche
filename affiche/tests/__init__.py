import os
import unittest
from .. import create_app, db


TEST_DB = 'test.db'
app = create_app()

class TestEnv(unittest.TestCase):
	def setUp(self):
		basedir = os.path.abspath(os.path.dirname(__file__))
		app.config['TESTING'] = True
		app.config['WTF_CRSF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,TEST_DB)
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		self.app = app.test_client()
		db.create_all()
		self.assertEqual(app.debug, False)

	def tearDown(self):
		db.drop_all()


if __name__ == '__main__':
	unittest.main()
