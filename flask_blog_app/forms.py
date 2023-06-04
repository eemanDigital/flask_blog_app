#wtf library will handle form management
from flask_wtf import FlaskForm
from wtforms  import StringField, PasswordField, SubmitField, BooleanField 
#manage conditions for validation of user inputs
from wtforms.validators import DataRequired, Length, Email, EqualTo

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


class LoginForm(FlaskForm):
    #set validation/requirements for login inputs
    # username = StringField('Username',  
    #                         validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remeberme = BooleanField('Remember Me')
    submit = SubmitField('Login')