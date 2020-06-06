from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_mail

users = Blueprint('users', __name__)

@users.route('/register',methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account is created for {form.username.data}!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)

@users.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(email=form.email.data).first().username
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('users.account'))  if next_page else redirect(url_for('main.home'))
                #flash(f' Welcome {username}!','success')
        else :
            flash(f'Login failed. Please check email and password','danger')
    return render_template('login.html',title='Login', form= form)
        # if form.email.data =='admin@blog.com' and form.password.data=='password':
        #     flash(f'you have been logged in !','success')
        #     return redirect(url_for('home'))
        # elif form.email.data =='admin@blog.com':
        #     flash(f'Login failed. Please check password ','danger')
        # elif form.password.data=='password':
        #     flash(f'Login failed. Please check email ','danger')
        # else:
        #
    return render_template('login.html',title='login',form=form)
@users.route('/logout',methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    
# Account setup

@users.route('/account',methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.imagef = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account has been updated succesfully!','success')
        redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static',filename ='profile_pics/'+current_user.imagef)
    return render_template('account.html',title='Account',imagef= image_file,form=form)
    
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',default=1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts =Post.query.filter_by(Author=user).order_by(Post.date_posted.desc()).paginate(page = page ,per_page = 5)
    return render_template('user_posts.html', posts= posts,user=user)


@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send mail to this user
        send_reset_mail(user)
        flash('Email reset link has been sent to your register mail', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title = 'Reset password',form =form)

@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is  None:
        flash("that is invalid or expired token",'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_password
        db.session.commit()
        flash(f'your password has been reset!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='reset password',form=form)
