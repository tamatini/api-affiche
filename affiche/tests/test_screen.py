from affiche.tests import TestEnv
import json


url = '/screen/'
screen_1 = {
	'screen_size': '17',
	'screen_resolution': '1920x1080',
	'screen_type': 'tft'
}

screen_2 = {
	'screen_size': '15.4',
	'screen_resolution': '1650x960',
	'screen_type': 'led'
}

content_type = 'application/json'


def new_screen(self,*args):
	return self.app.post(url, data=json.dumps(*args), content_type=content_type)


class ScreenPageTest(TestEnv):
	def test_screenpage_return_ok(self):
		response = self.app.get(url)
		self.assertEqual(response.status_code, 200)


class ScreenPostTest(TestEnv):
	def test_post_new_screen(self):
		response = new_screen(self, screen_1)
		self.assertIn(b"1920x1080" , response.data)
		self.assertEqual(201, response.status_code)

	def test_post_same_screen_error(self):
		new_screen(self, screen_1)
		response = new_screen(self, screen_1)
		self.assertEqual(400, response.status_code)


class ScreenTestById(TestEnv):
	def test_id_error_404(self):
		response = self.app.get(url+"id=1")
		self.assertEqual(404, response.status_code)

	def test_id_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.get(url+"id=1")
		self.assertEqual(200, response.status_code)

	def test_delete_id_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.delete(url+'id=1')
		self.assertEqual(200, response.status_code)
		response = self.app.delete(url+'id=1')
		self.assertEqual(404, response.status_code)

	def test_update_id_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.put(url+'id=1', data=json.dumps(screen_2), content_type=content_type)
		self.assertEqual(201, response.status_code)
		self.assertIn(b"15", response.data)
		response = self.app.put(url+'id=2', data=json.dumps(screen_2), content_type=content_type)
		self.assertEqual(404, response.status_code)

class ScreenTestBySize(TestEnv):
	def test_size_error_404(self):
		response = self.app.get(url+"size=17")
		self.assertEqual(404, response.status_code)

	def test_size_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.get(url+"size=17")
		self.assertEqual(200, response.status_code)

class ScreenTestByResolution(TestEnv):
	def test_resolution_error_404(self):
		response = self.app.get(url+"reso=1920x1080")
		self.assertEqual(404, response.status_code)

	def test_resolution_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.get(url+"reso=1920x1080")
		self.assertEqual(200, response.status_code)


class ScreenTestByType(TestEnv):
	def test_type_error_404(self):
		response = self.app.get(url+"type=tft")
		self.assertEqual(404, response.status_code)

	def test_type_return_ok(self):
		new_screen(self, screen_1)
		response = self.app.get(url+"type=tft")
		self.assertEqual(200, response.status_code)