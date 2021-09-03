from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_blog import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(userID: int):
	return User.query.get(int(userID))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	privilege_level = db.Column(db.Integer, nullable=False, default=4)
	posts = db.relationship('Post', backref='author', lazy=True)


	def get_reset_token(self, expires_sec=1800):
		jsonWebSerializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return jsonWebSerializer.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		jsonWebSerializer = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = jsonWebSerializer.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"{self.__class__.__name__}('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	is_modified = db.Column(db.Boolean, default=False, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"{self.__class__.__name__}('{self.title}', '{self.date_created}')"