from flask import Flask
from config import Config

# blueprints
from .auth.routes import auth
from .logs.routes import logs
from .company.routes import company
from .customer.routes import customer
from .equipment.routes import equipment

# db
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager

# API CORS
from flask_cors import CORS

app = Flask(__name__)
login = LoginManager()
CORS(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(auth)
app.register_blueprint(logs)
app.register_blueprint(company)
app.register_blueprint(customer)
app.register_blueprint(equipment)

app.config.from_object(Config)

db.init_app(app)
login.init_app(app)

login.login_view = "auth.logIn"

migrate = Migrate(app, db)

from . import routes
from . import models