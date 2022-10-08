from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from sqlalchemy_utils import create_database, database_exists


app = Flask(__name__)

# app.config.from_pyfile("config.py")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pls_db.db"

# app.config["SECRET_KEY"] = ""

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from my_project import routes

from my_project.models import Lotto,Winner,Staker,Jackpot,currentJackpot, currentLotto , SportsBots, User, SportBot
# db.drop_all()
db.create_all()
db.session.commit()




