from flask import url_for
from flask_blog.models import User

def get_profile_picture(user: User):
	flnm = user.image_file if hasattr(user, 'image_file') else 'default.jpg'
	profile_picture = url_for('static', filename='profile_pictures/{}'.format(flnm))
	return profile_picture