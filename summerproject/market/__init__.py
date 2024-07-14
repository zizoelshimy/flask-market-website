#this is __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize Flask application
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disable tracking modifications
app.config['SECRET_KEY'] = '759e70c91889643a9d9c1a29'
# Initialize SQLAlchemy
db = SQLAlchemy(app)

login_manager = LoginManager(app)

bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'loginpage'
login_manager.login_message_category = 'info'# this line is to change the login message to info as pretty one when we redirect to login page 
from market import models, routes


