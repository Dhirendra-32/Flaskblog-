from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
posts = Blueprint('posts', __name__)

@posts.route('/Post/new',methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,Author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created ','success')
        return redirect(url_for('main.home'))
        
    return render_template('create_post.html',title='new post',form=form,legend='New')

@posts.route('/Post/<int:post_id>',methods=['GET', 'POST'])
def post (post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)
    
@posts.route('/Post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post (post_id):
    post = Post.query.get_or_404(post_id)
    if post.Author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Post has been updated succesfully','success')
        return redirect(url_for('posts.post',post_id=post.id))
        
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('create_post.html',title ='Update',form=form,legend='Update')
@posts.route('/Post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post (post_id):
    post = Post.query.get_or_404(post_id)
    if post.Author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted !', category='info')
    return redirect(url_for('main.home'))
    
