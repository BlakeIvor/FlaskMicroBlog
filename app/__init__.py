from flask import Flask
from config import Config
import os
import logging
from logging.handlers import RotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
print(f"Static folder path: {os.path.join(app.root_path, 'static')}")

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = LoginManager(app)
manager.login_view = 'login'

# Register the user_loader callback from models.py
from app.models import load_user
manager.user_loader(load_user)

from app import routes, models, errors

if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')