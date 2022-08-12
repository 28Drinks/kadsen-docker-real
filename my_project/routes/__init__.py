from my_project import app
from flask import Flask, render_template, jsonify, request

from . import lotto_history , market_sport
from my_project.get_stats import get_stats


#home page
@app.route("/home")
def home():

    lotto_amount, jackpot_amount, btc_count = get_stats()


    return render_template("home.html", page_title="Enchanced Lottery", lotto_amount=lotto_amount, jackpot_amount=jackpot_amount, btc_count=btc_count)


@app.route('/_add_numbers')
def add_numbers():
    share = 1
    bet = 20
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=share / 100 * a * 12 + bet / 100 * b * 12 / 2)


@app.route('/')
def index():
    return render_template('index.html')
