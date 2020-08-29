from affiche.tests import TestEnv
import json


url_computer = "/computer/"
url_brand = "/brand/"
url_graphics = "/graphics/"
url_hdd = "/hardrive/"
url_memory = "/memory/"
url_proc = "/processor/"
url_screen = "/screen/"

computer_1 = {'model': 'Aspire A515-54G-542A', 'brand_id': 1, 'graphics_id': 1, 'processor_id': 1,
              'memory_id': 1, 'harddrive_id': 1, 'screen_id': 1, 'wifi': "802.11ac", 'bluetooth': 'oui',
			  'weight': 1.80, 'cdrom': 'oui', 'usb2': 1, 'usb3': 2, 'usbC': 0, 'hdmi': 'oui', 'vga': 'oui',
			  'prix': 119990, 'prix_promo': 109990, 'ean': 1234567891}
computer_2 = {'model': 'Aspire A515-54G-542A', 'brand_id': 1, 'graphics_id': 1, 'processor_id': 1,
              'memory_id': 1, 'harddrive_id': 1, 'screen_id': 1, 'wifi': "802.11ac", 'bluetooth': 'oui',
			  'weight': 1.80, 'cdrom': 'oui', 'usb2': 1, 'usb3': 2, 'usbC': 0, 'hdmi': 'oui', 'vga': 'oui',
			  'prix': 99990, 'prix_promo': 69990, 'ean': 1234567891}
brand = {'brandname': 'Acer'}
graphics = {'graphics_brand': 'Nvidia', 'graphics_model': 'GeForce MX250', 'graphics_memory':2}
hdd = {'hdd_type':'SSD', 'hdd_capacity': 512}
memory = {'memory_capacity':8, 'memory_type': 'DDR4', 'memory_frequency': '3400'}
proc =  {'proc_brand': 'Intel', 'proc_model': 'i5', 'proc_frequency': 1.6, 'proc_core': 1,
         'proc_thread': 4}
screen = {'screen_size': 15.6, 'screen_resolution': '1920x1080', 'screen_type':'tf'}
content_type = 'application/json'


def create_all(self):
	self.app.post(url_brand, data=json.dumps(brand), content_type=content_type)
	self.app.post(url_graphics, data=json.dumps(graphics), content_type=content_type)
	self.app.post(url_hdd, data=json.dumps(hdd), content_type=content_type)
	self.app.post(url_memory, data=json.dumps(memory), content_type=content_type)
	self.app.post(url_proc, data=json.dumps(proc), content_type=content_type)
	self.app.post(url_screen, data=json.dumps(screen), content_type=content_type)


def new_computer(self, *args):
	create_all(self)
	return self.app.post(url_computer, data=json.dumps(*args), content_type=content_type)


class ComputerPageTest(TestEnv):
	def test_computer_page_return_ok(self):
		response = self.app.get(url_computer)
		self.assertEqual(200, response.status_code)


class ComputerPostTest(TestEnv):
	def test_post_new_computer(self):
		response = new_computer(self, computer_1)
		self.assertEqual(201, response.status_code)

	def test_post_same_computer_error(self):
		new_computer(self, computer_1)
		response = new_computer(self, computer_1)
		self.assertEqual(400, response.status_code)

class ComputerTestById(TestEnv):
	def test_id_error_404(self):
		response = self.app.get(url_computer+'id=1')
		self.assertEqual(404, response.status_code)

	def test_id_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+"id=1")
		self.assertEqual(200, response.status_code)

	def test_id_update_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.put(url_computer+'id=1', data=json.dumps(computer_2), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"69990", response.data)

	def test_id_delete_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.delete(url_computer+'id=1')
		self.assertEqual(201, response.status_code)


class ComputerTestByModel(TestEnv):
	def test_model_error_404(self):
		response = self.app.get(url_computer+'model=Aspire A515-54G-542A')
		self.assertEqual(404, response.status_code)

	def test_model_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+"model=Aspire A515-54G-542A")
		self.assertEqual(200, response.status_code)


class ComputerTestByBrand(TestEnv):
	def test_brand_error_404(self):
		response = self.app.get(url_computer+'brand=Acer')
		self.assertEqual(404, response.status_code)

	def test_brand_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+"brand=Acer")
		self.assertEqual(200, response.status_code)

class ComputerTestByGraphics(TestEnv):
	def test_graphics_brand_error_404(self):
		response = self.app.get(url_computer+'graphics=Nvidia')
		self.assertEqual(404, response.status_code)

	def test_graphics_brand_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+"graphics=Nvidia")
		self.assertEqual(200, response.status_code)

	def test_graphics_model_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+"graphics=GeForce MX250")
		self.assertEqual(200, response.status_code)

class ComputerTestByEan(TestEnv):
	def test_ean_return_ok(self):
		new_computer(self, computer_1)
		response = self.app.get(url_computer+'ean=1234567891')
		self.assertEqual(200, response.status_code)

	def test_ean_return_error_404(self):
		response = self.app.get(url_computer+'ean=1234567891')
		self.assertEqual(404, response.status_code)