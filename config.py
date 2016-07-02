import os

SECRET_KEY = 'whatever'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI ='sqlite:///'+os.path.join(basedir,'data.sqlite')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'p.perlepes@gmail.com'
FLASKY_ADMIN = 'p.perlepes@gmail.com'
MAIL_PASSWORD = 'p.perlepes'
FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'