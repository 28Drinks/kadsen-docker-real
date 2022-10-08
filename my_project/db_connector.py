from my_project import db
from my_project.models import Winner, Staker, Lotto, Jackpot, currentJackpot, currentLotto, SportsBotsClean, SportsShare, SportBot
from datetime import datetime, timedelta

today = datetime.today()
yesterday = datetime.now() - timedelta(days=1)
tomorrow = datetime.now() + timedelta(days=1)


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

    def write_sportsbots_data_to_db(data):
        for a in data:
            newBot = SportsBotsClean(
                name=a["name"],
                image=a["image_url"],
                token_id=a["token_id"]
            )
            db.session.add(newBot)
            db.session.commit()

    def write_share_data_to_db(data):
        for a in data:
            newShare = SportsShare(
                sport=a,
                combined_share_value=data[a][0],
                base_share_value=data[a][1],
                bots_quantity=data[a][2],
                share_quantity=data[a][3],
                date=today
            )
            db.session.add(newShare)
            db.session.commit()

    def write_os_sportbot_data_to_db(data):
        for a in data:
            try:
                newBot = SportBot(
                    name = a["name"],
                    image_url = a["image_url"],
                    revealed = a["revealed"],
                    sportshares = a["sportshares"],
                    freebet = a["freebet"],
                    comboboost = a["comboboost"],
                    body = a["body"],
                    sport = a["sport"],
                    eyes = a["eyes"],
                    teeth = a["teeth"]
                )
            except:
                newBot = SportBot(
                    name = a["name"],
                    image_url = a["image_url"],
                    revealed = a["revealed"]
                )
            db.session.add(newBot)
            db.session.commit()

 