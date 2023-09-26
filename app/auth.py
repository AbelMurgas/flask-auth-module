from flask import Blueprint, request, jsonify, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import jwt
import datetime

# Create a Flask Blueprint for authentication
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    """
    Handle user login.

    This route accepts a POST request with user credentials (username and password) 
    in the request body. It verifies the credentials, generates a JSON Web Token (JWT) 
    if the login is successful, and returns the token as a response.

    Request JSON:
    {
        "user": "username",
        "password": "password"
    }

    Returns:
    - 200 OK: Login successful with JWT token.
    - 400 Bad Request: If required fields are missing, user not found, or incorrect password.
    """
    data = request.get_json()
    errors = {}

    # Check for required fields
    required_fields = ['user', 'password']
    for field in required_fields:
        if field not in data:
            errors[field] = f"{field.capitalize()} is required"

    if errors:
        return jsonify({'errors': errors}), 400

    user = User.query.filter_by(user=data['user']).first()

    if not user:
        return jsonify({'error': 'User not found'}), 400

    if not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Incorrect password'}), 400

    # Generate a JWT token
    secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, secret_key, algorithm='HS256')

    response = {'message': 'Login successful', 'token': token}
    return jsonify(response), 200

@auth.route('/sign-up', methods=["POST"])
def sign_up():
    """
    Handle user registration.

    This route accepts a POST request with user registration data (username, password, and first_name) 
    in the request body. It checks if the user already exists, and if not, creates a new user record 
    in the database.

    Request JSON:
    {
        "user": "username",
        "password": "password",
        "first_name": "John"
    }

    Returns:
    - 200 OK: Signup successful with a success message.
    - 400 Bad Request: If required fields are missing or if the user already exists.
    """
    data = request.get_json()
    errors = {}

    # Check for required fields
    required_fields = ['user', 'password', 'first_name']
    for field in required_fields:
        if field not in data:
            errors[field] = f"{field.capitalize()} is required"
    
    if errors:
        return jsonify({'errors': errors}), 400

    user = data['user']
    password = data['password']
    first_name = data['first_name']

    # Check if the user already exists
    user_found = User.query.filter_by(user=data['user']).first()
    if user_found:
        return jsonify({'error': 'This user already exists'}), 400

    # Create a new user record
    new_user = User(user=user, password=generate_password_hash(password=password, method='sha256'), first_name=first_name)
    db.session.add(new_user)
    db.session.commit()

    response = {'message': 'Signup successful', 'user': user}
    return jsonify(response), 200
