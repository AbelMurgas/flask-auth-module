from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """
    User Model for the application.

    This class defines the User model used in the application. It extends the `UserMixin` 
    class from Flask-Login to provide user authentication-related functionality.

    Attributes:
        id (int): The unique identifier for each user.
        user (str): The username for the user, must be unique.
        password (str): The hashed password for the user.
        first_name (str): The first name of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))