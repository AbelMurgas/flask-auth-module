import os

# Get the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Example to add additional configuration
class Config:
    """
    Base configuration class for the application.

    This class defines the base configuration settings for the application.
    It includes settings like the secret key and SQLAlchemy configuration.

    Attributes:
        SECRET_KEY (str): The secret key used for session and data security.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Controls whether to track modifications in SQLAlchemy.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_ultra_secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Example of how to set up different database configurations for different stages
class DevelopmentConfig(Config):
    """
    Configuration class for development stage.

    This class extends the base Config class and adds specific settings for
    the development stage, including database configuration.

    Attributes:
        DEBUG (bool): Controls whether the application runs in debug mode.
        DB_NAME (str): The name of the development database.
        SQLALCHEMY_DATABASE_URI (str): The URI for connecting to the development database.
    """
    DEBUG = True
    DB_NAME = "development.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'

class TestingConfig(Config):
    """
    Configuration class for testing stage.

    This class extends the base Config class and adds specific settings for
    the testing stage, including database configuration.

    Attributes:
        TESTING (bool): Controls whether the application is in testing mode.
        DB_NAME (str): The name of the test database.
        SQLALCHEMY_DATABASE_URI (str): The URI for connecting to the test database.
    """
    TESTING = True
    DB_NAME = "test.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'

class ProductionConfig(Config):
    """
    Configuration class for production stage.

    This class extends the base Config class and adds specific settings for
    the production stage, including database configuration.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The URI for connecting to the production database.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# Dictionary mapping configuration names to their respective classes
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}