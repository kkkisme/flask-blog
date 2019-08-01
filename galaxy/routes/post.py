from flask_login import login_required, current_user
from flask import request, Blueprint, render_template, redirect, url_for, flash, abort, current_app
from ..models.post import PostForm, Post
from .. import db
post = Blueprint('post', __name__)


@post.route('/post', methods=['GET'])
def post_home():
    return 'post'


@post.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        flash(message='Your post has been created!', category='success')
        return redirect(url_for('main.home'))
    return render_template('views/create_post.html', title='New Post', form=form)


@post.route('/post/<int:post_id>', methods=['GET'])
def single_post(post_id):
    p = Post.query.get_or_404(post_id)
    return render_template('views/post.html', title=p.title, post=p)


@post.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    p = Post.query.get_or_404(post_id)
    if p.author != current_user:
        abort(403)
    if form.validate_on_submit():
        p.title = form.title.data
        p.content = form.content.data
        db.session.commit()
        flash(message='Your post has been updated!', category='success')
        return redirect(url_for('post.single_post', post_id=p.id))
    form.title.data = p.title
    form.content.data = p.content
    form.submit.label.text = 'Update'
    return render_template('views/create_post.html', title='Update Post', form=form, legend='Update Post')


@post.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    p = Post.query.get_or_404(post_id)
    if p.author != current_user:
        abort(403)
    db.session.delete(p)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
