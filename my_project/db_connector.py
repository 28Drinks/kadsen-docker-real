from my_project import db
from my_project.models import Winner, Staker, Lotto, Jackpot, currentJackpot, currentLotto

class DbWriter():
    @staticmethod
    def write_winner_data_to_db(data):
        for a in data:
            newWinner = Winner(
            position=a["position"],
            name=a["name"],
            amount=a["amount"]
            )
            db.session.add(newWinner)
            db.session.commit()
    def write_staker_data_to_db(data):
        for a in data:
            newStaker = Staker(
            name=a["name"],
            amount=a["amount"],
            team=a["team"]
            )
            db.session.add(newStaker)
            db.session.commit()
    # need to create / import db model "Lotto","Jackpot"
    def write_lotto_stats_to_db(data):
        for a in data:
            updateLotto = currentLotto(
            number=a["number"],
            amount=a["amount"],
            at_time=a["at_time"]
            )
            db.session.add(updateLotto)
            db.session.commit()
    def write_jackpot_stats_to_db(data):
        for a in data:
            updateJackpot = currentJackpot(
            amount=a["amount"],
            at_time=a["at_time"]
            )
            db.session.add(updateJackpot)
            db.session.commit()