import jwt
from functools import wraps
from flask import request, jsonify, current_app
from .models import User  # Adjust the import as needed

def token_required(f):
    """
    Decorator to protect routes by requiring a valid JWT token.

    This decorator checks for the presence of a JWT token in the 'Authorization' header 
    of the incoming request. It verifies the token's validity and decodes it to obtain 
    the user's ID. If the token is valid, it retrieves the current user and passes it 
    as an argument to the decorated route function.

    Args:
        f (function): The decorated route function.

    Returns:
        function: The decorated route function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            secret_key = current_app.config['SECRET_KEY']
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401

        return f(current_user, *args, **kwargs)

    return decorated