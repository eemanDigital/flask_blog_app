#wtf library will handle form management
from flask_wtf import FlaskForm

from wtforms  import StringField, SubmitField,TextAreaField
# from flask_wtf.file import FileField, FileAllowed
#manage conditions for validation of user inputs
from wtforms.validators import DataRequired

#form for new posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    #picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')