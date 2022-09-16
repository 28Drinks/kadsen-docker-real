from datetime import datetime
from enum import unique
from my_project import db, login_manager, bcrypt
from flask_login import ( UserMixin )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#lottery model
class Lotto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    date = db.Column(db.String)
    amount = db.Column(db.Integer)
    jackpot = db.Column(db.Integer)
    prizes_won = db.Column(db.String)
    total_stake = db.Column(db.String)
    index_key = db.Column(db.Integer)

#currentLottery model
class currentLotto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    at_time = db.Column(db.DateTime, default=datetime.utcnow)


#winner model
class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String)
    name = db.Column(db.String)
    team = db.Column(db.String)
    amount = db.Column(db.Integer)
    image = db.Column(db.String)


#staker model
class Staker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team = db.Column(db.String)
    amount = db.Column(db.Integer)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotto.id'))

#jackpot model
class Jackpot(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jackpot_total = db.Column(db.Integer())
    date = db.Column(db.String)

#currentjackpot model
class currentJackpot(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jackpot_total = db.Column(db.Integer())
    at_time = db.Column(db.DateTime, default=datetime.utcnow)

#sportsbots
class SportsBots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    name = db.Column(db.String)
    display_share = db.Column(db.String)
    bet = db.Column(db.String)
    token_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    roi = db.Column(db.Integer)

class SportsBotsClean(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    name = db.Column(db.String)
    token_id = db.Column(db.Integer)
    selected_by = db.Column(db.Integer(), db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=35), nullable=False ,unique=True)
    email_address = db.Column(db.String(length=40), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=40), nullable=False)
    bots = db.relationship(
        "SportsBotsClean", backref="selected_bots", lazy=True
    )

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class SportsShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String)
    value = db.Column(db.Float)
    date = db.Column(db.Date)





