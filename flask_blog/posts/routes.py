from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, jsonify
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post, Replies
from flask_blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/<int:post_id>')
def post(post_id: int):
	post = Post.query.get_or_404(post_id)
	replies = Replies.query.filter_by(post_id=post.id).order_by(Replies.date_created.asc())
	return render_template('post.html', title=post.title, post=post, replies=replies)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Post posted.', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post', legend='New Post', form=form)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def updatePost(post_id: int):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user and current_user.privilege_level >= 1:
		abort(403)
	form = PostForm()
	# from wtforms.widgets.core.py line 259
	form.submit.label.text = 'Update'
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		post.is_modified = True
		db.session.commit()
		flash('Post successfully updated.', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id: int):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user and current_user.privilege_level >= 1:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted.', 'success')
	return redirect(url_for('main.home'))


@posts.route('/reply', methods=['POST'])
@login_required
def replyPost():
	post_id = request.form.get('post_id', type=int)
	replyContent = request.form.get('reply_content')
	print(post_id, replyContent)
	if post_id and replyContent:
		reply = Replies(post_id=post_id, content=replyContent, user_id=current_user.id)
		db.session.add(reply)
		db.session.commit()
		return jsonify({'success':True})
	return jsonify({'success':False})


@posts.route('/reply/delete', methods=['POST'])
@login_required
def deleteReply():
	reply_id = request.form.get('reply_id', type=int)
	if reply_id:
		reply = Replies.query.get_or_404(reply_id)
		if reply.author != current_user and current_user.privilege_level >= 1:
			abort(403)
		db.session.delete(reply)
		db.session.commit()
		return jsonify({'success':True})
	return jsonify({'success':False})
