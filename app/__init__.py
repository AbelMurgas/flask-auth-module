from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from .config import config_dict

db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config_dict[config_name])
  db.init_app(app)

  from .auth import auth
  app.register_blueprint(auth, url_prefix="/auth/")

  from .models import User
  

  create_database(app)

  return app

def create_database(app):
  with app.app_context():
    if not path.exists('app/' + app.config["DB_NAME"]):
      db.create_all()