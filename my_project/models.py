from datetime import datetime
from my_project import db

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







