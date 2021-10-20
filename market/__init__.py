from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SECRET_KEY'] = 'c72c6dc55741ce3e40667084'

db = SQLAlchemy(app)

ma = Marshmallow(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from market import routes



