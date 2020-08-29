from affiche.tests import TestEnv


class MainPageTest(TestEnv):
	def test_main_page(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

