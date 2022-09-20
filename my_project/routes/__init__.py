from my_project import app
from flask import Flask, render_template, jsonify, request
import json
from my_project import db
from my_project.models import SportsShare
from . import sports_share
# from my_project.get_stats import get_stats


#home page - old stuff
# @app.route("/home")
# def home():
#     lotto_amount, jackpot_amount, btc_count = get_stats()

#     return render_template("home.html", page_title="Enchanced Lottery", lotto_amount=lotto_amount, jackpot_amount=jackpot_amount, btc_count=btc_count)



@app.route("/")
@app.route("/landing_page")
def landing_page():

    return render_template("landing_page.html", page_title="Landing Page")
