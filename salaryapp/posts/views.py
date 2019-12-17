# POSTS/VIEWS.PY
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from siteapp import db
from salaryapp.models import Post
from salaryapp.posts.forms import PostForm

posts = Blueprint('posts', __name__)

# CREATE A POST
@posts.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():

        post = Post(title=form.title.data, text=form.text.data, user_id=current_user.id)

        db.session.add(post)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

# VIEW A POST
@posts.route('/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, date=post.date, text=post.text, post=post)

# UPDATE A POST
@posts.route("/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('posts.post', post_id=post.id))
    # Pass back the old post information so they can start again with the old text and title.
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
    return render_template('create_post.html', title='Update', form=form)

# DELETE A POST
@posts.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('core.index'))
