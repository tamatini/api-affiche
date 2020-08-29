from affiche.tests import TestEnv
import json


url = '/processor/'
processor_1 = {
	'proc_brand': 'intel',
	'proc_model': 'i7',
	'proc_frequency': 3500,
	'proc_core': 4,
	'proc_thread': 8
}

processor_2 = {
	'proc_brand': 'AMD',
	'proc_model': '3600',
	'proc_frequency': 3500,
	'proc_core': 4,
	'proc_thread': 12
}

content_type = 'application/json'

def new_processor(self, *args):
	return self.app.post(url, data=json.dumps(*args), content_type=content_type)


class ProcessorPageTest(TestEnv):
	def test_processor_page_ok(self):
		response = self.app.get(url)
		self.assertEqual(200, response.status_code)


class ProcessorPostTest(TestEnv):
	def test_post_new_processor(self):
		response = new_processor(self, processor_1)
		self.assertIn(b"3500", response.data)
		self.assertEqual(201, response.status_code)

	def test_post_same_processor_error(self):
		new_processor(self, processor_1)
		response = new_processor(self, processor_1)
		self.assertEqual(400, response.status_code)


class ProcessorTestById(TestEnv):
	def test_id_error_404(self):
		response = self.app.get(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_id_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'id=1')
		self.assertEqual(200, response.status_code)

	def test_delete_id_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.delete(url+'id=1')
		self.assertEqual(200, response.status_code)
		response = self.app.delete(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_update_id_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.put(url+'id=1', data=json.dumps(processor_2), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"12", response.data)
		response = self.app.put(url+'id=2', data=json.dumps(processor_2), content_type=content_type)
		self.assertEqual(404, response.status_code)


class MemoryTestBybrand(TestEnv):
	def test_brand_return_error_404(self):
		response = self.app.get(url+'brand=intel')
		self.assertEqual(404, response.status_code)

	def test_brand_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'brand=intel')
		self.assertEqual(200, response.status_code)


class MemoryTestByModel(TestEnv):
	def test_model_return_error_404(self):
		response = self.app.get(url+'model=i7')
		self.assertEqual(404, response.status_code)

	def test_model_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'model=i7')
		self.assertEqual(200, response.status_code)


class MemoryTestByFrequency(TestEnv):
	def test_frequency_return_error_404(self):
		response = self.app.get(url+'frequency=3500')
		self.assertEqual(404, response.status_code)

	def test_frequency_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'frequency=3500')
		self.assertEqual(200, response.status_code)

	def test_frequency_return_all_processor(self):
		new_processor(self, processor_1)
		new_processor(self, processor_2)
		response = self.app.get(url+'frequency=3500')
		self.assertIn(b"i7", response.data)
		self.assertIn(b"3600", response.data)


class MemoryTestByCore(TestEnv):
	def test_core_return_error_404(self):
		response = self.app.get(url+'core=4')
		self.assertEqual(404, response.status_code)

	def test_core_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'core=4')
		self.assertEqual(200, response.status_code)


class MemoryTestByThread(TestEnv):
	def test_thread_return_error_404(self):
		response = self.app.get(url+'thread=8')
		self.assertEqual(404, response.status_code)

	def test_thread_return_ok(self):
		new_processor(self, processor_1)
		response = self.app.get(url+'thread=8')
		self.assertEqual(200, response.status_code)