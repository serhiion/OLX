from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from server.configs import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from server.models.models import User, Advertisements

with app.app_context():
    db.create_all()

from server.routes import routes
