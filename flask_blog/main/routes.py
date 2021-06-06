from flask import Blueprint, render_template, request, url_for
from flask_blog.models import Post


main = Blueprint('main', __name__)


@main.route("/")
def home():
	page = request.args.get('page', 1, type=int)
	limit = min(request.args.get('limit', 5, type=int), 100)
	posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=limit)
	return render_template('home.html', posts=posts)


@main.route('/about')
def about():
	return render_template("about.html", title='About')




# ----- UNIQUE ----- #
@main.route('/favicon.ico')
def favicon():
	return url_for('static', filename='favicon.ico')