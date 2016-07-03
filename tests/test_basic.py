import unittest
from flask import current_app
from app import create_app, db
from app.models import User

class BasicTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		self.assertIsNotNone(current_app)

	def test_app_test_env(self):
		self.assertTrue(current_app.config['TESTING'])

class UserModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.user = User(password = 'password')

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_password_setter(self):
		self.assertIsNotNone(self.user.password_hash)

	def test_password_getter(self):
		with self.assertRaises(AttributeError):
			self.user.password

	def test_password_verify(self):
		self.assertTrue(self.user.verify_password('password'))

	def test_password_random_salt(self):
		user2 = User(password = 'password')
		self.assertNotEqual(self.user.password_hash, user2.password_hash)