from blog import app, db, User, Post

# Create a Flask application instance
# app = create_app()

# Use the application context
with app.app_context():
    # Create a user object
    user_1 = User(username='john_doe', email='john@example.com', password='password123')

    # Add the user object to the session
    db.session.add(user_1)

    # Commit the changes to the database
    db.session.commit()

    users = User.query.all()
    for user in users:
        print(user.username)