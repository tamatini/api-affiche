from affiche.tests import TestEnv
import json

url = '/graphics/'
content_type="application/json"
post_graphics = {
	'graphics_brand':'nvidia',
	'graphics_model':'RTX1080',
	'graphics_memory':'8'
}

def new_graphics(self):
	post_new_graphics = self.app.post(
		url,
		data=json.dumps(post_graphics),
		content_type=content_type)
	return post_new_graphics


class GraphicsPageTest(TestEnv):
	def test_graphics_page_return_status_code_200(self):
		response = self.app.get(url)
		self.assertEqual(200, response.status_code)

	def test_post_new_graphics_return_status_code_201(self):
		response = new_graphics(self)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"nvidia", response.data)

	def test_post_same_graphics_return_error(self):
		new_graphics(self)
		response=new_graphics(self)
		self.assertEqual(400, response.status_code)
		self.assertIn(b"Cette carte graphique existe", response.data)


class GraphicsTestByBrand(TestEnv):
	def test_get_all_graphics_by_brand(self):
		new_graphics(self)
		response = self.app.get(url+'brand=nvidia')
		self.assertEqual(200, response.status_code)
		self.assertIn(b"nvidia", response.data)

	def test_get_all_graphics_by_brand_return_error_404(self):
		response = self.app.get(url+'brand=nvidia')
		self.assertEqual(404, response.status_code)
		self.assertIn(b"Pas de carte graphique de cette marque", response.data)

class GraphicsTestByModel(TestEnv):
	def test_get_graphics_by_model(self):
		new_graphics(self)
		response = self.app.get(url+'model=RTX1080')
		self.assertEqual(200, response.status_code)
		self.assertIn(b"RTX1080", response.data)

	def test_get_graphics_by_model_return_error_404(self):
		response = self.app.get(url+'model=RTX1080')
		self.assertEqual(404, response.status_code)
		self.assertIn(b"Cette carte graphique n'existe pas", response.data)


class GraphicsTestById(TestEnv):
	def test_get_graphics_by_id(self):
		new_graphics(self)
		response = self.app.get(url+'id=1')
		self.assertEqual(200, response.status_code)

	def test_get_graphics_by_id_return_error_404(self):
		response = self.app.get(url+'id=1')
		self.assertEqual(404, response.status_code)
		self.assertIn(b"Cette carte graphique n'existe pas", response.data)

	def test_update_graphics_by_id(self):
		new_graphics(self)
		response = self.app.put(
			url+'id=1',data=json.dumps({
				'graphics_model':'RTX2080',
				'graphics_brand':'nvidia'}),
		content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"RTX2080", response.data)

	def test_delete_graphics_by_id(self):
		new_graphics(self)
		response = self.app.delete(url+'id=1')
		self.assertEqual(201, response.status_code)

	def test_delete_graphics_by_id_return_404(self):
		response = self.app.delete(url+'id=1')
		self.assertEqual(404, response.status_code)