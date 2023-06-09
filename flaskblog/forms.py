#wtf library will handle form management
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms  import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
#manage conditions for validation of user inputs
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError 
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    #set validation/requirements for username registration
    username = StringField('Username',  
                            validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #custom form validation to check existing username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist')

    #custom form validation to check existing email
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exist')


class LoginForm(FlaskForm):
    #set validation/requirements for login inputs
    # username = StringField('Username',  
    #                         validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


    #Handles update of Account
class UpdateAccountForm(FlaskForm):
    #set validation/requirements for username registration
    username = StringField('Username',  
                                validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    #manages profile pic
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

#custom form validation to check existing username
def validate_username(self, username):
    if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist')

    #custom form validation to check existing email
def validate_email(self, email):
    if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exist')
        
#form for new posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validator=[DataRequired()])
    submit = SubmitField('Post')
