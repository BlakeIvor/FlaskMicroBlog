from flask import Flask
from config import Config
import os

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

from app import routes, models