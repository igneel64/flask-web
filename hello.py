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
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
import config

basedir = os.path.abspath(os.path.dirname(__file__))
#ADD TO GIT, TEST ASSETS AND TIME, COMPLETE FORMS AND EXPERIMENT WITH ALL


app = Flask('flask-web')
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = config.SQLALCHEMY_COMMIT_ON_TEARDOWN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = config.FLASKY_MAIL_SUBJECT_PREFIX
app.config['FLASKY_MAIL_SENDER'] = config.FLASKY_MAIL_SENDER
app.config['FLASKY_ADMIN'] = config.FLASKY_ADMIN
mail = Mail(app)
manager = Manager(app)
moment = Moment(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


def make_shell_context():
	return dict(app = app, db = db, Role = Role, User = User)

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

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject, sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)

@app.route('/', methods = ['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if not user:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			import pdb;pdb.set_trace()
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'], 'New user', 'mail/new_user', user = user)
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
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	db.create_all()
	manager.run()
