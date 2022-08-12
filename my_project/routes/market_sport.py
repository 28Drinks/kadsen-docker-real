from contextlib import redirect_stderr
from tkinter.tix import Select

# from requests import Session
import operator
import sqlalchemy
from sqlalchemy import desc
from my_project import app
from flask import Flask, render_template, jsonify, request , url_for , redirect
from my_project import db
from my_project.get_sportbots import get_sportbots
from my_project.models import SportsBots

# @app.route('/add_bots')
# def add_bots():
#     sportbots = SportsBots.query.all()

#     return(sportbots)

@app.route("/", methods=["GET", "POST"])
def bots_page():
    return render_template("index.html")


@app.route("/sportbots", methods=["GET", "POST"])
def sportbots_page():
    bot_list = SportsBots.query.all()
    bot_dict_list = []

    for bot in bot_list:
        image=bot.image
        name=bot.name
        share=bot.display_share
        bet=bot.bet
        price=bot.price
        roi=bot.roi

        bot_dict_list.append({ "image": image, "name": name, "share": share, "bet": bet, "price": price, "roi": roi})

    bot_list_price_asce = bot_dict_list

    bot_list_price_desc = sorted(bot_dict_list, key=lambda d: d['price'], reverse=True)

    bot_list_bet_asce = sorted(bot_dict_list, key=lambda d: d["bet"])

    bot_list_bet_desc = sorted(bot_dict_list, key=lambda d: d["bet"], reverse=True)



    return render_template("sportbots.html", page_title="Market Sniper 28",
     sportbots_price_asce=bot_list_price_asce,
     sportbots_price_desc=bot_list_price_desc,
     sportbots_bet_asce=bot_list_bet_asce,
     sportbots_bet_desc=bot_list_bet_desc)
