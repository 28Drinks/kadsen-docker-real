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
    if request.method == "POST":
        text = request.form['text']
        processed_text = "Sportsbot #" + text
        bot = SportBot.query.filter(SportBot.name == processed_text).first()

        share_object = SportsShare.query.filter(SportsShare.sport == bot.sport).order_by(SportsShare.date.desc()).first()

        if bot.sport is not None:
            base_share = share_object.base_share_value
            bot_share = base_share * bot.sportshares

            r_freebet = bot.freebet * 12 / 2
            r_share = bot_share * 12
            r_total = r_freebet + r_share

            price = r_total * 2.5

            return render_template("roi-result.html", pagetitle="ROI", bot=bot, base_share=base_share,price=("%.2f" % price), bot_share=("%.2f" % bot_share),r_freebet=("%.2f" % r_freebet),r_share=("%.2f" % r_share),r_total=("%.2f" % r_total))

        else:
            return render_template("roi-result.html", bot=bot)

    
    return render_template("roi.html", pagetitle="ROI")