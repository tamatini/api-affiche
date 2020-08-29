from affiche.tests import TestEnv
import json


url = '/brand/'
brandname = {'brandname': 'test'}
content_type = 'application/json'


def new_brand(self):
	return self.app.post(url, data=json.dumps(brandname), content_type=content_type)


class BrandPageTest(TestEnv):
	def test_brand_page_return_code_200(self):
		response = self.app.get(url)
		self.assertEqual(response.status_code, 200)


class BrandPostTest(TestEnv):
	def test_post_new_brand(self):
		response = new_brand(self)
		self.assertIn(b"test", response.data)
		self.assertEqual(201, response.status_code)

	def test_post_same_brand_error(self):
		new_brand(self)
		response = new_brand(self)
		self.assertEqual(400, response.status_code)


class BrandTestByBrandname(TestEnv):
	def test_brandname_return_error_404(self):
		response = self.app.get(url+'brandname=test')
		self.assertEqual(404, response.status_code)

	def test_brandname_return_ok(self):
		new_brand(self)
		response = self.app.get(url+'brandname=test')
		self.assertEqual(200, response.status_code)


class BrandTestById(TestEnv):
	def test_id_without_post_return_error_404(self):
		response = self.app.get(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_id_return_status_code_201(self):
		response = new_brand(self)
		self.assertEqual(201, response.status_code)
		self.assertIn(b'test', response.data)

	def test_update_by_id(self):
		new_brand(self)
		response = self.app.put(url+'id=1', data=json.dumps({'brandname': 'test_2'}), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"test_2", response.data)

	def test_delete_by_id(self):
		new_brand(self)
		response=self.app.delete(url+'id=1')
		self.assertEqual(201, response.status_code)

