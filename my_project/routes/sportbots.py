from cProfile import label
from collections import defaultdict
from my_project import app
from flask import render_template, jsonify, request
from my_project import db
from my_project.models import SportBot, SportsShare
from flask import request


from datetime import datetime, timedelta

import matplotlib.pyplot as plt

@app.route("/roi", methods=["GET", "POST"])
def roi():
    def calculateReturn(bet,share,bet_setting,share_setting):
        bet_return = bet * 12 * ( bet_setting / 100)
        share_return = share * 12 * ( share_setting / 100)
        total_return = bet_return + share_return
        price = total_return * 2.5

        print(bet,share,bet_setting,share_setting)

        return_values = {"bet_return" : bet_return, "share_return": share_return, "total_return": total_return, "price": price}
        return return_values

    if request.method == "POST":
        try:
            bot_number = request.form.get('input_bot_number') or 28
            share_setting = request.form.get('share_setting') or 100
            bet_setting = request.form.get('bet_setting') or 50

            processed_number = int(bot_number) + 1
            bot = SportBot.query.filter(SportBot.id == processed_number).first()

            share_object = SportsShare.query.filter(SportsShare.sport == bot.sport).order_by(SportsShare.date.desc()).first()


            if bot.sport is not None:
                base_share = share_object.base_share_value
                bot_share = base_share * bot.sportshares
                
                return_values_calculated = calculateReturn(int(bot.freebet), float(bot_share), float(bet_setting), float(share_setting))


                return render_template("roi-result.html", pagetitle="ROI", bot=bot,bot_number=bot_number, share_setting=share_setting, bet_setting=bet_setting, return_values_calculated=return_values_calculated, base_share=base_share, bot_share=("%.2f" % bot_share))

        except:
            return render_template("roi-result.html", bot=bot)


        else:
            # need to make this better, for now set variables to 0 for unrevealed bot
            return render_template("roi-result.html", bot=bot, return_values_calculated={"bet_return" : 0, "share_return": 0, "total_return": 0, "price": 0}, share_setting=0, bet_setting=0)

    
    return render_template("roi.html", pagetitle="ROI")