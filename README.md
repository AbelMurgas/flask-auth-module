# Flask Auth Module

The Flask Auth Module is a Python-based authentication system designed to provide robust authentication mechanisms, ensuring the security of your users' data and controlled access. This module is thoroughly tested for code reliability and maintainability using Coverage.py and Pytest. It leverages JSON Web Tokens (JWT) for secure and efficient authentication.

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/AbelMurgas/flask-auth-module

cd flask-auth-module
```

### 2. Create a virtual environment and activate it (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The Flask Auth Module uses different configurations for development, testing, and production stages. To configure the application, you can set the following environment variables or modify the config.py file:


*SECRET_KEY*: The secret key for session and data security. <br>
*SQLALCHEMY_DATABASE_URI*: The URI for the database connection.
Example environment variable configuration:

```bash
SECRET_KEY = "super_secret"
SQLALCHEMY_DATABASE_URI = "database.db"
```

## Usage
### Running the Application
To run the Flask Auth Module, execute the following command:

```bash
python app.py
```
The application will start in debug mode and can be accessed at http://localhost:5000.

## API Endpoints
### User Registration
To register a new user, send a POST request to /auth/sign-up with the following JSON data:

```json
{
    "user": "your_username",
    "password": "your_password",
    "first_name": "Your First Name"
}
```
### User Login
To log in as a registered user, send a POST request to /auth/login with the following JSON data:

```json
{
    "user": "your_username",
    "password": "your_password"
}
```
The login endpoint will return a JWT token upon successful authentication.

## Testing
We ensure code quality and reliability through automated testing. To run the tests, use the following command:

```bash
pytest
```
Coverage reports are generated automatically and can be found in the htmlcov directory.

To run coverage to testing, and report 
```bash
coverage run -m pytest
coverage report
```

If you want to access the html report format, you must use the following code:

```bash
coverage html
```

## Contributing
We welcome contributions! Feel free to open issues or submit pull requests to help improve the Flask Auth Module.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
