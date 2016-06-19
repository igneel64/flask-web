import unittest
import hello

class HelloTestCase(unittest.TestCase):
	def setUp(self):
		hello.app.testing = True
		self.app = hello.app.test_client()

	def test_home(self):
		rv = self.app.get('/')
		assert b'Hello World' in rv.data
	
	def test_user_agent_restriction(self):
		rv = self.app.get('/user/Dave', follow_redirects = True)
		self.assertIn(b'Hello World', rv.data)

	def test_user_agent_allowance(self):
		rv = self.app.get('/user/Dave',headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'} ,follow_redirects = True)
		self.assertIn(b'Hello, Dave', rv.data)


if __name__=='__main__':
	unittest.main()