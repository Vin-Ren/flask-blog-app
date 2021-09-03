from flask import url_for
from flask_blog.models import User

def get_profile_picture(user: User):
	profile_picture = url_for('static', filename=f'profile_pictures/{user.image_file}')
	return profile_picture