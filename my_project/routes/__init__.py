from my_project import app
from flask import Flask, render_template, jsonify, request
from flask_login import current_user
import json
from my_project import db
from my_project.models import SportsShare
from . import lotto_history , market_sport, my_bots, auth
# from my_project.get_stats import get_stats

from datetime import datetime, timedelta


import matplotlib.pyplot as plt

today1 = datetime.today()
today = today1.strftime('%Y-%m-%d')
yesterday1 = datetime.now() - timedelta(days=1)
yesterday = yesterday1.strftime('%Y-%m-%d')


#home page - old stuff
# @app.route("/home")
# def home():
#     lotto_amount, jackpot_amount, btc_count = get_stats()

#     return render_template("home.html", page_title="Enchanced Lottery", lotto_amount=lotto_amount, jackpot_amount=jackpot_amount, btc_count=btc_count)



@app.route("/")
@app.route("/landing_page")
def landing_page():

    share_data_today = SportsShare.query.filter(SportsShare.date == today).order_by(SportsShare.value.desc()).all()
    share_data_yesterday = SportsShare.query.filter(SportsShare.date == yesterday).order_by(SportsShare.value.desc()).all()

    change = {}
    percentage = {}
    for t,y in zip(share_data_today, share_data_yesterday):
        # print(t.sport,t.value,y.sport,y.value)
        sport = t.sport
        change_value = t.value -y.value
        percent = ((t.value - y.value) / y.value) * 100
        percentage[sport] = round(percent, 2)
        change[sport] = round(change_value, 2)

    black_list = ["total"]
    labels = [x.sport for x in share_data_today if x.sport not in black_list]
    values = [x.value for x in share_data_today if x.sport not in black_list]


    return render_template("landing_page.html", page_title="Landing Page", share_data=share_data_today, percentage=percentage, change=change, labels=labels, values=values)
