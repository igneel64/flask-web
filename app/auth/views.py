from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..email import send_email
from .. import db

@auth.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username or password')
	return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email = form.email.data, username = form.username.data, password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email,'Confirm your account', 'auth/email/confirm', user = user, token = token)
		flash('A confirmation email has been sent to your email address.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form = form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flask('Your account has been confirmed.')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authnticated():
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] != 'auth.':
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email('auth/email/confirm', 'Confirm your account', user, token = token)
	flash('A new confirmation email has been sent to you by email.')
	#make it threaded
	return redirect(url_for('main.index'))

@auth.route('/update', methods = ['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			 current_user.password = form.password.data
			 db.session.add(current_user)
			 flash('Password updated successfuly!')
			 return redirect(url_for('main.index'))
		else:
			flash('Invalid password.')
	return render_template('auth/updatePassword.html', form = form)


@auth.route('/reset', methods = ['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			token = user.generate_confirmation_token()
			send_email(user.email, 'Reset your password', 'auth/email/reset_password',
			user = user, token = token, next = request.args.get('next'))
		flash('An email to reset your password has been sent to your email')
		return redirect(url_for('auth.login'))
	return render_template('auth/updatePassword.html', form = form)

@auth.route('/reset/<token>', methods = ['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.date).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.password.data):
			flash('Your password has been updated.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form = form)

@auth.route('/change-email', methods = ['GET', 'POST'])
@login_required
def change_email_request():
	form = ChangeEmailForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.email.data
			token = current_user.generate_email_change_token(new_email)
			send_email(new_email, 'Confirm your email address', 'auth/email/change_email',
						user = current_user, token = token)
			flash('An email with the instructions to confirm your new email address has been sent to you')
			return (url_for('main.index'))
		else:
			flash('Invalid password.')
	return render_template('auth/change_email.html', form = form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
	if current_user.change_email(token):
		flash('Your email address has been updated.')
	else:
		flash('Invalid request.')
	return redirect(url_for('main.index'))





