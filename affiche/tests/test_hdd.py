from affiche.tests import TestEnv
import json

url = "/hardrive/"
hdd = {
	'hdd_type': 'SSD',
	'hdd_capacity': '512'
}

hdd_up = {
	'hdd_type': 'HDD',
	'hdd_capacity': '256'
}

content_type="application/json"

def new_hdd(self):
	return self.app.post(url, data=json.dumps(hdd), content_type=content_type)


class HddPageTest(TestEnv):
	def test_hdd_page_return_code_200(self):
		response = self.app.get(url)
		self.assertEqual(200, response.status_code)

	def test_post_new_hdd(self):
		response = new_hdd(self)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"SSD", response.data)

	def test_post_same_hdd_return_400(self):
		new_hdd(self)
		response = new_hdd(self)
		self.assertEqual(400, response.status_code)
		self.assertIn(b"Ce disque existe", response.data)


class HddTestByType(TestEnv):
	def test_hdd_by_type_return_200(self):
		new_hdd(self)
		response = self.app.get(url+'type=SSD')
		self.assertEqual(200, response.status_code)


	def test_hdd_by_type_return_error_400(self):
		response = self.app.get(url+'type=SSD')
		self.assertEqual(404, response.status_code)


class HddTestByCapacity(TestEnv):
	def test_hdd_by_capacity_return_200(self):
		new_hdd(self)
		response = self.app.get(url+'capacity=512')
		self.assertEqual(200, response.status_code)

	def test_hdd_by_capacity_return_error_404(self):
		response = self.app.get(url+'capacity=512')
		self.assertEqual(404, response.status_code)

class HddTestById(TestEnv):
	def test_hdd_by_id_return_200(self):
		new_hdd(self)
		response = self.app.get(url+'id=1')
		self.assertEqual(200, response.status_code)

	def test_hdd_by_id_return_error_404(self):
		response = self.app.get(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_update_hdd_by_id(self):
		new_hdd(self)
		response = self.app.put(url+'id=1', data=json.dumps(hdd_up), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"HDD", response.data)
		self.assertIn(b"256", response.data)

	def test_update_hdd_by_id_error_404(self):
		response = self.app.put(url+'id=1', data=json.dumps(hdd_up), content_type=content_type)
		self.assertEqual(404, response.status_code)