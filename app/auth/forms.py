from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

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

class ChangePasswordForm(Form):
	current_password = PasswordField('Current password', validators = [Required()])
	new_password = PasswordField('New password', validators = [Required(), Length(8,64), EqualTo('new_password_retype', message = 'Passwords must match.')])
	new_password_retype = PasswordField('Retype new password', validators = [Required(), Length(8,64)])
	submit = SubmitField('Update password')

class PasswordResetRequestForm(Form):
	email = StringField('Type your email.', validators = [Required(), Length(1, 64), Email()])
	submit = SubmitField('Reset password.')

class PasswordResetForm(Form):
	email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators = [Required(), Length(8, 64), EqualTo('password2', message = 'Passwords must match.')])
	password2 = PasswordField('Confirm password', validators = [Required(), Length(8, 64)])
	submit = SubmitField('Reset password.')

	def validate_email(self, field):
			if User.query.filter_by(email = field.data).first():
				raise ValidationError('Unknown email.')

class ChangeEmailForm(Form):
	email = StringField('New email', validator = [Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators = [Required()])	
	submit = SubmitField('Update email address')

	def validate_email(self, field):
		if User.query.filter_by(emal=field.data).first():
			raise ValidationError('Email already registered.')



