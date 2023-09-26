import json
import pytest
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@pytest.fixture
def client():
    """
    Create a test client for the app.

    This fixture sets up a Flask test client for testing the application.
    It creates a testing database, sets up the application context, and drops
    the database after testing.

    Returns:
        FlaskClient: A test client for making HTTP requests to the app.
    """
    app = create_app("testing")

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_registration_successful(client):
    """
    Test user registration with valid data.

    This test case simulates a successful user registration with valid data.
    It sends a POST request to the registration endpoint with valid user data
    and checks if the response indicates a successful registration.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # Prepare the test data for the POST request
    data = {'user': 'newuser', 'password': 'password123', 'first_name': 'John'}

    # Make a POST request to the registration endpoint
    response = client.post('/auth/sign-up', json=data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check if the response message indicates successful registration
    assert response.json['message'] == 'Signup successful'

def test_registration_duplicate_username(client):
    """
    Test user registration with a duplicate username.

    This test case simulates a user registration attempt with a username that
    already exists in the database. It sends a POST request to the registration
    endpoint with a duplicate username and checks if the response indicates an
    error due to the duplicate username.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # --- Prepare a user with the same username ---
    existing_user = User(user='existinguser', password=generate_password_hash(
        password='password123', method='sha256'))
    db.session.add(existing_user)
    db.session.commit()

    # Prepare the test data with a duplicate username
    data = {'user': 'existinguser', 'password': 'password456', 'first_name': 'Jane'}

    # Make a POST request to the registration endpoint
    response = client.post('/auth/sign-up', json=data)

    # Check if the response status code is 400 (bad request) indicating duplicate username
    assert response.status_code == 400
    assert 'error' in response.json

def test_authentication_successful(client):
    """
    Test user authentication with valid credentials.

    This test case simulates a successful user login with valid credentials.
    It sends a POST request to the login endpoint with correct username and
    password and checks if the response includes a valid JWT token.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # --- Prepare a user with known credentials ---
    test_user = User(user='testuser', password=generate_password_hash(
        password='hashed_password', method='sha256'))
    db.session.add(test_user)
    db.session.commit()

    # Prepare the test data for the POST request
    data = {'user': 'testuser', 'password': 'hashed_password'}

    # Make a POST request to the login endpoint
    response = client.post('/auth/login', json=data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    # Check if the response contains a 'token' key
    assert 'token' in response.json

def test_authentication_invalid_credentials(client):
    """
    Test user authentication with invalid credentials.

    This test case simulates a user login attempt with incorrect credentials.
    It sends a POST request to the login endpoint with an incorrect password
    and checks if the response indicates an error due to incorrect credentials.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # --- Prepare a user with known credentials ---
    test_user = User(user='testuser', password=generate_password_hash(
        password='hashed_password', method='sha256'))
    db.session.add(test_user)
    db.session.commit()

    # Prepare the test data with incorrect password
    data = {'user': 'testuser', 'password': 'incorrect_password'}

    # Make a POST request to the login endpoint
    response = client.post('/auth/login', json=data)

    # Check if the response status code is 400 (bad request) indicating incorrect credentials
    assert response.status_code == 400
    assert 'error' in response.json

def test_missing_required_fields_login(client):
    """
    Test user login with missing required fields.

    This test case simulates a user login attempt with missing required fields
    (e.g., 'user' or 'password'). It sends POST requests to the login endpoint
    with missing fields and checks if the response indicates errors for missing
    fields.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # Prepare a JSON payload with missing 'user' field
    data = {'password': 'password123'}

    # Make a POST request to the login endpoint with missing fields
    response = client.post('/auth/login', json=data)

    # Check if the response status code is 400 (bad request)
    assert response.status_code == 400

    # Check if the response contains an error message for the missing field
    assert 'errors' in response.json
    assert 'User is required' == response.json['errors']['user']

    # Repeat the same test for missing 'password' field
    data = {'user': 'testuser'}
    response = client.post('/auth/login', json=data)
    assert response.status_code == 400
    assert 'errors' in response.json
    assert 'Password is required' == response.json['errors']['password']

def test_duplicate_user(client):
    """
    Test user registration with a duplicate username.

    This test case simulates a user registration attempt with a username that
    already exists in the database. It sends a POST request to the registration
    endpoint with a duplicate username and checks if the response indicates an
    error due to the duplicate username.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # --- Prepare a user with the same username ---
    existing_user = User(user='testuser', password=generate_password_hash(
        password='password123', method='sha256'))
    db.session.add(existing_user)
    db.session.commit()

    # Prepare a JSON payload with an existing username
    data = {'user': 'testuser', 'password': 'newpassword', 'first_name': 'John'}

    # Make a POST request to the sign-up endpoint with an existing username
    response = client.post('/auth/sign-up', json=data)

    # Check if the response status code is 400 (bad request)
    assert response.status_code == 400

    # Check if the response contains an error message for duplicate username
    assert 'error' in response.json
    assert 'This user already exists' == response.json['error']

def test_missing_required_fields_sign_up(client):
    """
    Test user registration with missing required fields.

    This test case simulates a user registration attempt with missing required
    fields (e.g., 'user' or 'password'). It sends POST requests to the registration
    endpoint with missing fields and checks if the response indicates errors for
    missing fields.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    # Prepare a JSON payload with missing 'user' field
    data = {'password': 'password123'}

    # Make a POST request to the login endpoint with missing fields
    response = client.post('/auth/sign-up', json=data)

    # Check if the response status code is 400 (bad request)
    assert response.status_code == 400

    # Check if the response contains an error message for the missing field
    assert 'errors' in response.json
    assert 'User is required' == response.json['errors']['user']

    # Repeat the same test for missing 'password' field
    data = {'user': 'testuser'}
    response = client.post('/auth/sign-up', json=data)
    assert response.status_code == 400
    assert 'errors' in response.json
    assert 'Password is required' == response.json['errors']['password']

def test_user_not_found(client):
    """
    Test user login with a user that does not exist.

    This test case simulates a user login attempt with a username that does not
    exist in the database. It sends a POST request to the login endpoint with
    a non-existent username and checks if the response indicates an error.

    Args:
        client (FlaskClient): The test client for making HTTP requests.

    Returns:
        None
    """
    data = {'user': 'notfound', 'password': 'password456'}

    # Make a POST request to the login endpoint
    response = client.post('/auth/login', json=data)

    assert 'error' in response.json
    assert 'User not found' == response.json['error']

    # Check if the response status code is 400 (bad request) indicating user not found
    assert response.status_code == 400
    assert 'error' in response.json