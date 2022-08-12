from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'

db = SQLAlchemy(app)



from my_project.models import Lotto,Winner,Staker,Jackpot,currentJackpot, currentLotto , SportsBots
# db.drop_all()
db.create_all()
db.session.commit()

from my_project import routes


