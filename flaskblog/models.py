<<<<<<< HEAD
from datetime import datetime,timedelta
#from itsdangerous import URLSafeTimedSerializer as Serializer
import jwt
from itsdangerous import URLSafeTimedSerializer as Serializer
=======
from datetime import datetime 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
>>>>>>> refs/remotes/origin/main
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

<<<<<<< HEAD
#method to create token
# def get_reset_token(self, expires_sec=1800):
#     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     return s.dumps({'user_id': self.id}).decode('utf-8')
# def get_reset_token(self):
#     """Generates a reset token for the user."""
#     token = jwt.encode({
#         "id": self.id,
#         "exp": datetime.datetime.utcnow() + timedelta(days=1),
#     }, app.config["SECRET_KEY"])
#     return token


#method to verify token
# @staticmethod#remove self as an argument
# def verify_reset_token(token):
#    # Create a Serializer object with the application's secret key.
#    s = Serializer(app.config['SECRET_KEY'])
#    try:
#         user_id = s.loads(token)['user_id']
#    except:
#         return None
#    # Return the user object if the user ID is valid.
#    return User.query.get(user_id)


def get_reset_token(self):
    """Generates a reset token for the user."""
    token = jwt.encode({
        "id": self.id,
        "exp": datetime.datetime.utcnow() + timedelta(days=1),
    }, app.config["SECRET_KEY"])
    return token

def verify_reset_token(token):
   """Verifies a reset token and returns the user object if it is valid."""
   # Create a Serializer object with the application's secret key.
   s = Serializer(app.config['SECRET_KEY'])
   try:
        user_id = s.loads(token)['user_id']
   except:
        return None
   # Return the user object if the user ID is valid.
   return User.query.get(user_id)







def __repr__(self):
    return f"User('{self.username}', {self.email}, '{self.image_file}')"
=======
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
>>>>>>> refs/remotes/origin/main

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # post_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
