from . import db

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

class User(Base):
	__tablename__ = 'users'
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username