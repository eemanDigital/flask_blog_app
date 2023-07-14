#wtf library will handle form management
from flask_wtf import FlaskForm

from wtforms  import StringField, SubmitField,TextAreaField
#manage conditions for validation of user inputs
from wtforms.validators import DataRequired

#form for new posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')