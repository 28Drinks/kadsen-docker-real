from hashlib import new
from my_project import app
from flask import Flask, render_template, jsonify, request
import json
from my_project import db
from my_project.models import SportsShare
from . import sports_share, sportbots

from datetime import datetime, timedelta


# from my_project.get_stats import get_stats


#home page - old stuff
# @app.route("/home")
# def home():
#     lotto_amount, jackpot_amount, btc_count = get_stats()

#     return render_template("home.html", page_title="Enchanced Lottery", lotto_amount=lotto_amount, jackpot_amount=jackpot_amount, btc_count=btc_count)



@app.route("/")
@app.route("/landing_page")
def landing_page():

    today1 = datetime.today()
    today = today1.strftime('%Y-%m-%d')
    yesterday1 = datetime.now() - timedelta(days=1)
    yesterday = yesterday1.strftime('%Y-%m-%d')

    black_list = ["total"]

    all_share_data_today = SportsShare.query.filter(SportsShare.date == today).order_by(SportsShare.combined_share_value.desc()).all()
    all_share_data_yesterday = SportsShare.query.filter(SportsShare.date == yesterday).order_by(SportsShare.combined_share_value.desc()).all()


    top_moover_percent = {}
    top_moover_dollar = {}

    for today,yesterday in zip(all_share_data_today, all_share_data_yesterday):
        if today.sport not in black_list:
            sport = today.sport
            change_value = today.combined_share_value - yesterday.combined_share_value
            change_percent = ((today.combined_share_value - yesterday.combined_share_value) / yesterday.combined_share_value) * 100
            top_moover_percent[sport] = round(change_percent, 2)
            top_moover_dollar[sport] = round(change_value, 2)

    #sort low to high for %
    top_moover_percent = sorted(top_moover_percent.items(), key=lambda item: item[1])
    highest_percent = list(top_moover_percent)[0]
    lowest_percent = list(top_moover_percent)[-1]

    #sort low to high for $
    top_moover_dollar = sorted(top_moover_dollar.items(), key=lambda item: item[1])
    lowest_dollar = list(top_moover_dollar)[0]
    highest_dollar = list(top_moover_dollar)[-1]

    #top 4 sports by combined share value
    top_sports = [x for x in all_share_data_today[:5] if x.sport not in black_list]

    movement_dict = {"lowest_percent": lowest_percent, "highest_percent": highest_percent, "lowest_dollar": lowest_dollar, "highest_dollar": highest_dollar}

    return render_template("landing_page.html", page_title="Landing Page", movement_dict=movement_dict, top_sports=top_sports[:4])



@app.route("/reources_page")
def resources_page():

    return render_template("resources.html", pagetitle="Resources")