from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm, 
                             UpdateAccountForm,RequestResetForm, ResetPasswordForm)
from flaskblog.models import User
from flaskblog.users.utils import send_reset_email, save_picture
from flask_login import login_user, current_user, logout_user, login_required



users = Blueprint('users', __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
    #deny user access to register page after logging in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         #password hashing for authentication
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
         #create database
         db.create_all()
        #add to database
         db.session.add(user)
         db.session.commit()
         #flash user upon creation of account
         flash(f"Accounted Created for {form.username.data}", category='success')
         return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods=['GET', 'POST'])
def login():
    #deny user access to login page after logging in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         #if user exist, log in
         if user and bcrypt.check_password_hash(user.password, form.password.data):
             login_user(user, remember=form.remember.data)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect(url_for('main.home'))
         else:
            flash('Sign in unsuccessfull, check your email and password', category='error')
    return render_template('login.html', form=form, title='Login')

#logout user
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


#user account route
@users.route('/account', methods=['GET', 'POST'])
@login_required #account only accesible on login
def account():
    form = UpdateAccountForm()#for account update
    if form.validate_on_submit():
        if form.picture.data:
            picture_file =save_picture(form.picture.data)
            current_user.image_file =  picture_file 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account successfuly updated', category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' 
                         + current_user.image_file)
    return render_template('account.html', title='Account Page',
                            image_file=image_file, form=form)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction on how to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
         #password hashing for authentication
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         #create database
        #  db.create_all()
        #add to database
         user.password = hashed_password
         db.session.commit()
         #flash user upon creation of account
         flash(f"Your password has been updated!", category='success')
         return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)




