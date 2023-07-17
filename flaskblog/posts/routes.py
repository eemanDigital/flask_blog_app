from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import User, Post
from flaskblog.users.utils import save_picture
from flask_login import login_required, current_user

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit() and form.picture.data:
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        picture_file =save_picture(form.picture.data)
        current_user.image_file =  picture_file 
        db.session.add(post)
        db.session.commit()
        flash('Post created!', category='success')
    image_file = url_for('static', filename='profile_pics/' 
                          + current_user.image_file)
    return render_template('create_post.html', image_file=image_file, title='New Post', 
                           form=form, legend='New Post')



    # if form.validate_on_submit():
    #     if form.picture.data:
    #         picture_file =save_picture(form.picture.data)
    #         current_user.image_file =  picture_file 
    #     current_user.username = form.username.data
    #     current_user.email = form.email.data
    #     db.session.commit()
    #     flash('Account successfuly updated', category='success')
    #     return redirect(url_for('account'))
    # elif request.method == 'GET':
    #     form.username.data = current_user.username
    #     form.email.data = current_user.email
    # image_file = url_for('static', filename='profile_pics/' 
    #                      + current_user.image_file)
    # return render_template('account.html', title='Account Page',
    #                         image_file=image_file, form=form)













@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

#update post
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'] )
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET'  :
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update  Post', 
                            form=form, legend='Update Post' )

#delete post
@posts.route('/post/<int:post_id>/delete', methods=['POST'] )
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', category='success')
    return redirect(url_for('main.home'))


#get posts of a user
@posts.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    #get user with the username
    user = User.query.filter_by(username=username).first_or_404()
    # posts= Post.query.all() #for all post
    posts= Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)
