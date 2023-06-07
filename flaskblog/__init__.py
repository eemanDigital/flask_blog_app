from flask import Flask
#handles database
from flask_sqlalchemy import SQLAlchemy
#import forms
#for user authentication
from flask_bcrypt import Bcrypt
#manages login activities
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b08874cb4837f88b0afb2f06202cae0e'
#set URI/PATH for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes
