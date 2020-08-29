from affiche.tests import TestEnv
import json


url = '/memory/'
memory_1 = {
	'memory_capacity': 4000,
	'memory_type': 'DDR4',
	'memory_frequency': 3500
}

memory_2 = {
	'memory_capacity': 2048,
	'memory_type': 'DDR3',
	'memory_frequency': 2400
}

content_type = 'application/json'

def new_memory(self, *args):
	return self.app.post(url, data=json.dumps(*args), content_type=content_type)


class MemoryPageTest(TestEnv):
	def test_memory_page_ok(self):
		response = self.app.get(url)
		self.assertEqual(200, response.status_code)


class MemoryPostTest(TestEnv):
	def test_post_new_memory(self):
		response = new_memory(self, memory_1)
		self.assertIn(b"4000", response.data)
		self.assertEqual(201, response.status_code)

	def test_post_same_memory_error(self):
		new_memory(self, memory_1)
		response = new_memory(self, memory_1)
		self.assertEqual(400, response.status_code)


class MemoryTestById(TestEnv):
	def test_id_error_404(self):
		response = self.app.get(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_id_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.get(url+'id=1')
		self.assertEqual(200, response.status_code)

	def test_delete_id_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.delete(url+'id=1')
		self.assertEqual(200, response.status_code)
		response = self.app.delete(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_update_id_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.put(url+'id=1', data=json.dumps(memory_2), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"2400", response.data)
		response = self.app.put(url+'id=2', data=json.dumps(memory_2), content_type=content_type)
		self.assertEqual(404, response.status_code)


class MemoryTestByCapacity(TestEnv):
	def test_capacity_return_error_404(self):
		response = self.app.get(url+'capacity=4000')
		self.assertEqual(404, response.status_code)

	def test_capacity_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.get(url+'capacity=4000')
		self.assertEqual(200, response.status_code)


class MemoryTestByType(TestEnv):
	def test_type_return_error_404(self):
		response = self.app.get(url+'type=DDR4')
		self.assertEqual(404, response.status_code)

	def test_type_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.get(url+'type=DDR4')
		self.assertEqual(200, response.status_code)


class MemoryTestByFrequency(TestEnv):
	def test_frequency_return_error_404(self):
		response = self.app.get(url+'frequency=3500')
		self.assertEqual(404, response.status_code)

	def test_frequency_return_ok(self):
		new_memory(self, memory_1)
		response = self.app.get(url+'frequency=3500')
		self.assertEqual(200, response.status_code)