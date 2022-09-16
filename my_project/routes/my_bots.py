from my_project import app
from flask import render_template
from my_project import db
from my_project.models import SportsBotsClean, User
from flask_login import login_required, current_user
import json

@app.route("/my_bots/<string:selectedBotsName>", methods=["POST"])
def ProcessSelectedInfo(selectedBotsName):
    selectedBots = json.loads(selectedBotsName)
    print(selectedBots[0])
    return('/')

@app.route("/my_bots")
@login_required
def my_bots_page():

    # bots_ids = User.query.filter_by(current_user).bots
    # user_selected_bots = SportsBots.query.filter_by(bots_ids)

    bot_list = SportsBotsClean.query.filter(SportsBotsClean.id < 100).all()
    bot_dict_list = []

    for bot in bot_list:
        id=bot.id
        image=bot.image
        name=bot.name

        bot_dict_list.append({ "image": image, "name": name,"id": id})

    return render_template("my_bots.html", page_title="My Bots", sportbots=bot_dict_list)