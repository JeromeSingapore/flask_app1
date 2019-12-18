#  __INIT__ FILE TO INITIALISE THE APPLICATION
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

##################################
### DATABASE SETUP ###############
##################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

db = SQLAlchemy(app)
Migrate(app, db)

##################################
### SETUP LOGIN CONFIG ###########
##################################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


from salaryapp.core.views import core
from salaryapp.users.views import users
# from siteapp.posts.views import posts
from salaryapp.error_pages.handlers import error_pages


app.register_blueprint(core)
app.register_blueprint(users)
# app.register_blueprint(posts)
app.register_blueprint(error_pages)
