import os
import hashlib
import secrets

from flask import current_app, url_for
from PIL import Image

from flask_blog import mail
from flask_blog.models import User
from flask_mail import Message


class Crypter:
	@staticmethod
	def default_hash(s, **kwargs):
		return s.decode('utf-8')
	
	def __init__(self, bcryptObject, additional_hash='sha1'):
		self.hash = self.select_hash(additional_hash)
		self.bcrypt = bcryptObject
		self.gen = self.generate_password_hash
		self.check = self.check_password_hash

	def change_hash(self, hash_name):
		self.hash = self.select_hash(hash_name)
		return self

	def select_hash(self, hash_name):
		hash_name = hash_name.lower()
		if hash_name == 'md5':
			return hashlib.md5
		elif hash_name == 'sha1':
			return hashlib.sha1
		elif hash_name == 'sha224':
			return hashlib.sha224
		elif hash_name == 'sha256':
			return hashlib.sha256
		elif hash_name == 'sha384':
			return hashlib.sha384
		elif hash_name == 'sha512':
			return hashlib.sha512
		return self.default_hash

	def generate_password_hash(self, password):
		pwd = self.hash(password.encode('utf-8'), usedforsecurity=True).hexdigest()
		hashed = self.bcrypt.generate_password_hash(pwd).decode('utf-8')
		return hashed

	def check_password_hash(self, hash, password):
		expected_pwd = self.hash(password.encode('utf-8'), usedforsecurity=True).hexdigest()
		return self.bcrypt.check_password_hash(hash, expected_pwd)



def resize_image(img:Image.Image, maxShorterLen=250):
	width, height = img.size
	if width < height:
		img = img.resize((maxShorterLen, int(maxShorterLen/width * height)))
	else:
		img = img.resize((int(maxShorterLen/height * width), maxShorterLen))
	return img


def save_picture(profile_picture):
	randHex = secrets.token_hex(8)
	fileExt = profile_picture.filename.split('.')[-1]
	picture_filename = f"{randHex}.{fileExt}"
	picturePath = os.path.join(current_app.root_path, 'static/profile_pictures', picture_filename)

	maxDimension = (1000, 1000)
	img: Image.Image = Image.open(profile_picture)

	img = resize_image(img, max(maxDimension))
	width, height = img.size
	left, top, right, bottom = 0,0,width,height
	if width > maxDimension[0]:
		left, right = (width - maxDimension[1])/2, width - ((width - maxDimension[1])/2)
	if height > maxDimension[1]:
		top, bottom = (height - maxDimension[0])/2, height - ((height - maxDimension[0])/2)
	img = img.crop((left, top, right, bottom))
	img.save(picturePath)
	return picture_filename


def send_reset_email(user: User):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply0flblog.reset.pwd@gmail.com', recipients=[user.email])
	msg.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

Please keep in mind that this link is only effective within 30 minutes of requesting.
If you did not make this request then simply ignore this email and no changes will be made to your account.
'''
	mail.send(msg)