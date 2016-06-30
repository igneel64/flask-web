import unittest
from flask_testing import TestCase
import hello

class HelloTestCase(TestCase):

	def create_app(self):
		app = hello.app
		app.testing = True
		return app

	def setUp(self):
		hello.app.testing = True
		self.app = hello.app.test_client()

	

	def test_404_page(self):
		rv = self.app.get('/Dave')
		self.assert404(rv)
		self.assertIn('Flasky - 404', rv.data)



if __name__=='__main__':
	unittest.main()