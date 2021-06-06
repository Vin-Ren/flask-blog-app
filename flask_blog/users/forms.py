from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from flask_login import current_user
from flask_blog.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username',
						   validators=[validators.DataRequired(),
									   validators.Length(min=2, max=20)])
	email = StringField('Email',
						validators=[validators.DataRequired(),
									validators.Email()])
	password = PasswordField('Password',
							 validators=[validators.DataRequired(),
										 validators.Length(min=2, max=15)])
	confirmPassword = PasswordField('Confirm Password',
									validators=[validators.DataRequired(),
												validators.EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise validators.ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(username=email.data).first()

		if user:
			raise validators.ValidationError('That email is taken. Please choose another one.')



class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[validators.DataRequired(),
									validators.Email()])
	password = PasswordField('Password',
							 validators=[validators.DataRequired(),
										 validators.Length(min=2, max=15)])
	rememberMe = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	profile_picture = FileField('New Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), FileSize(max_size=25*(1024**2))])
	username = StringField('New username',
						   validators=[validators.DataRequired(),
									   validators.Length(min=2, max=20)])
	email = StringField('New email',
						validators=[validators.DataRequired(),
									validators.Email()])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()

			if user:
				raise validators.ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(username=email.data).first()

			if email:
				raise validators.ValidationError('That email is taken. Please choose another one.')

class RequestResetPasswordForm(FlaskForm):
	email = StringField('Email',
						validators=[validators.DataRequired(),
									validators.Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()

		if not user:
			raise validators.ValidationError('There is no account bind to that email. You must register first.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',
							 validators=[validators.DataRequired(),
										 validators.Length(min=2, max=15)])
	confirmPassword = PasswordField('Confirm Password',
									validators=[validators.DataRequired(),
												validators.EqualTo('password')])
	submit = SubmitField('Reset Password')
