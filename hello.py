import os
from flask import Flask, request, make_response, redirect, url_for, render_template, session, flash
from flask_script import Manager, Server, Shell
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
#ADD TO GIT, TEST ASSETS AND TIME, COMPLETE FORMS AND EXPERIMENT WITH ALL


app = Flask('flask-web')
app.config.from_pyfile('config.cfg') #make from object
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'data.sqlite')
manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

def make_shell_context():
	return dict(app = app, db = db, Role = Role)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(64), unique = True, index = True)
	users = db.relationship('User', backref = 'role' , lazy = 'dynamic')
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username

class NameForm(Form):
	name = StringField('name', validators = [DataRequired()])
	submit = SubmitField('Submit')		

@app.route('/', methods = ['GET','POST'])
def index():
	import pdb;pdb.set_trace()
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if not user:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False) )


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


manager.add_command('debug', Server(host='0.0.0.0',port =5000, use_debugger = True, use_reloader = True))
manager.add_command('shell', Shell(make_context = make_shell_context))
if __name__ == '__main__':
	db.create_all()
	manager.run()
