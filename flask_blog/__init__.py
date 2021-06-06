from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	bcrypt.init_app(app)
	loginManager.init_app(app)
	mail.init_app(app)


	from flask_blog.utils import get_profile_picture
	# Add jinja_env.global, used when rendered, functions the same as passing kwargs to flask render_template,
	# It's just nicer if its used all around, and can be set once on globals.
	# Starting Point of search is in venv\Lib\site-packages\flask\templating.py then into __init__.py and to app.py
	# Got This From flask.app's code, in venv\Lib\site-packages\flask\app.py on lines: 677, 598, 803, and 1200
	app.jinja_env.globals.update({'get_profile_picture': get_profile_picture})


	from flask_blog.main.routes import main
	from flask_blog.users.routes import users
	from flask_blog.posts.routes import posts
	from flask_blog.errors.handlers import errors

	app.register_blueprint(main)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(errors)

	return app