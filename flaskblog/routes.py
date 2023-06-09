import secrets
from PIL import Image
import os
from flask import render_template, url_for, flash, redirect, request 
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts= [
        {
            'content':'This was revealed in a statement signed on Friday by the State House Director of Information', 
            'title': '1st Post', 
            'author': 'Adam',
            'date': '12/3/23'
            },
        {
            'content': 'Abiodun Oladunjoye, titled President Tinubu appoints Gbajabiamila COS, Sen. Ibrahim Hadejia,',
              'title': '2nd Post',
                'author': 'Chris',
                  'date': '2/3/23'
                },
        {
            'content': ' Kaduna Speaker hails Gbajabiamila',
            'title': '3rd Post', 
            'author': 'Munir',
            'date': '1/5/23'
            }
]

#Application routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=["GET", "POST"])
def register():
    #deny user access to register page after logging in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         #password hashing for authentication
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #create database
         db.create_all()
         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #add to database
         db.session.add(user)
         db.session.commit()
         #flash user upon creation of account
         flash(f"Accounted Created for {form.username.data}", category='success')
         return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #deny user access to login page after logging in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         #if user exist, log in
         if user and bcrypt.check_password_hash(user.password, form.password.data):
             login_user(user, remember=form.remember.data)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect(url_for('home'))
         else:
            flash('Sign in unsuccessfull, check your email and password', category='error')
    return render_template('login.html', form=form, title='Login')

#logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#save picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 
                                'static/profile_pics', picture_fn)
    #re-size image on upload
    ouput_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(ouput_size)
    i.save(picture_path)
    return picture_fn
    

#user account route
@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' 
                         + current_user.image_file)
    return render_template('account.html', title='Account Page',
                            image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        
    return render_template('create_post.html', title='New Post', form=form)