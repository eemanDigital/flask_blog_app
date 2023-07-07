import os
from flask import Flask
#handles database
from flask_sqlalchemy import SQLAlchemy
#import forms
#for user authentication
from flask_bcrypt import Bcrypt
#manages login activities
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b08874cb4837f88b0afb2f06202cae0e'
#set URI/PATH for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#this rectify the table not exist/context error
app.app_context().push()
 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#direct user to login page when trying to access account without login
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'#boostrap colour for message

#setting up mail server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flaskblog import routes
