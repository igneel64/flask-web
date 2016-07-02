import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = 'whatever'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	FLASKY_ADMIN = 'p.perlepes@gmail.com'
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_PASSWORD = 'p.perlepes'
	MAIL_USERNAME = 'p.perlepes@gmail.com'
	SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
	pass

config = {
	'development' : DevelopmentConfig,
	'testing' : TestingConfig,
	'production' : ProductionConfig,
	'default' : DevelopmentConfig
}

