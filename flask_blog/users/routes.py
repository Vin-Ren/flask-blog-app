from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import *
from flask_blog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created successfully.', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit() or request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.rememberMe.data)
			flash('Login Successful!', 'success')
			nextPage = request.args.get('next')
			return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
		flash('Login failed. Please check your email and password again.', 'danger')
	return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.profile_picture.data:
			current_user.image_file = save_picture(form.profile_picture.data)
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form=form)


@users.route("/user/<string:username>")
@users.route("/u/<int:user_id>")
@users.route("/u/<string:username>")
def userPosts(username=None, user_id=None):
	page = request.args.get('page', 1, type=int)
	limit = min(request.args.get('limit', 5, type=int), 100)
	if username:
		user = User.query.filter_by(username=username).first_or_404()
	elif user_id:
		user = User.query.get_or_404(user_id)
	else:
		return redirect(url_for('main.home'))
	posts = Post.query.filter_by(author=user)\
			.order_by(Post.date_created.desc())\
			.paginate(page=page, per_page=limit)
	#posts.reverse()
	return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def requestResetPassword():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.requestResetPassword'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Your password has been updated! You can now log in with your new credentials.', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)
