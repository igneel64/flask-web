from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo

class LoginForm(Form):
	email = StringField('Email', validators = [Required(), Email(), Length(1, 64)])
	password = PasswordField('Password', validators = [Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log in')

class RegisterForm(Form):
	email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
	username = StringField('Username', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must contain only letters, numbers, dots or underscores')])
	password = PasswordField('Password', validators = [Required(), Length(8, 64), EqualTo('password2', message = 'Passwords must match.')])
	password2 = PasswordField('Confirm password', validators = [Required(), Length(8, 64)])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username = field.data).first():
			raise ValidationError('Username already in use.')