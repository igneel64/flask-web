from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Base(db.Model):
	__abstract__ = True

	created_at = db.Column(db.DateTime, default = db.func.now())
	updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate = db.func.now())
	id = db.Column(db.Integer, primary_key = True)

class Role(Base):
	__tablename__ = 'roles'
	name = db.Column(db.String(64), unique = True)
	users = db.relationship('User', backref = 'role', lazy = 'dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, Base):
	__tablename__ = 'users'
	username = db.Column(db.String(64), unique = True, index = True)
	email = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User %r>' % self.username

	@property
	def password(self):
		raise AttributeError('Password is not readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)



@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
