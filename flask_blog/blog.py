from flask import Flask, render_template, url_for, flash, redirect 
#handles database
from flask_sqlalchemy import SQLAlchemy
#import forms
from forms import RegistrationForm, LoginForm
from models import User, Post

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b08874cb4837f88b0afb2f06202cae0e'
#set URI/PATH for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)



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
def home():
    return render_template('home.html', posts=posts, title='Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=["GET", "POST"])
def register():
     form = RegistrationForm()
     if form.validate_on_submit():
         flash(f"Accounted Created for {form.username.data}", category='success')
         return redirect(url_for('home'))
     return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
         flash('Sign in successfull', category='success')
         return redirect(url_for('home'))
     return render_template('login.html', form=form, title='Login')


if __name__ == '__main__':
    app.run(debug=True)