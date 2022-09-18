from cProfile import label
from collections import defaultdict
from my_project import app
from flask import render_template, jsonify, request
from my_project import db
from my_project.models import SportsShare

from datetime import datetime, timedelta

import matplotlib.pyplot as plt


@app.route("/share_today")
def share_today():

    today1 = datetime.today()
    today = today1.strftime('%Y-%m-%d')
    yesterday1 = datetime.now() - timedelta(days=1)
    yesterday = yesterday1.strftime('%Y-%m-%d')

    share_data_today = SportsShare.query.filter(SportsShare.date == today).order_by(SportsShare.combined_share_value.desc()).all()
    share_data_yesterday = SportsShare.query.filter(SportsShare.date == yesterday).order_by(SportsShare.combined_share_value.desc()).all()

    change_in_dollar = {}
    change_in_percentage = {}
    base_share_value = {}
    share_quantity = {}
    bots_quantity = {}
    for today,yesterday in zip(share_data_today, share_data_yesterday):
        # print(t.sport,t.value,y.sport,y.value)
        sport = today.sport
        change_value = today.combined_share_value -yesterday.combined_share_value
        change_percent = ((today.combined_share_value - yesterday.combined_share_value) / yesterday.combined_share_value) * 100
        change_in_percentage[sport] = round(change_percent, 2)
        change_in_dollar[sport] = round(change_value, 2)
        base_share_value[sport] = today.base_share_value
        share_quantity[sport] = today.share_quantity
        bots_quantity[sport] = today.bots_quantity

    black_list = ["total"]
    labels = [x.sport for x in share_data_today if x.sport not in black_list]
    values = [x.combined_share_value for x in share_data_today if x.sport not in black_list]


    return render_template("share_today.html", page_title="Share Today", share_data_today=share_data_today, change_in_percentage=change_in_percentage, change_in_dollar=change_in_dollar, base_share_value=base_share_value, share_quantity=share_quantity, bots_quantity=bots_quantity, labels=labels, values=values)


# not refactored
@app.route("/share_history")
def share_history():

    share_data = SportsShare.query.order_by(SportsShare.date.desc()).all()

    sport = [x.sport for x in share_data]
    date = [x.date.strftime('%Y-%m-%d') for x in share_data]
    base_share_value = [x.base_share_value for x in share_data]
    combined_value = [x.combined_share_value for x in share_data]

    share_data_dict = defaultdict(list)
    for sport,date,base_share,combined_share in zip(sport,date,base_share_value,combined_value):
        share_data_dict[sport].append([date,base_share,combined_share]) or ([date,base_share,combined_share])

    label = [x for x in share_data_dict]
    labels = []
    values_base = []
    values_combined = []
    for key in share_data_dict:
        labels.append([x[0] for x in share_data_dict[key]])
        values_base.append([x[1] for x in share_data_dict[key]])
        values_combined.append([x[2] for x in share_data_dict[key]])


    return render_template("share_history.html", page_title="Share History", label=label, labels=labels, values_base=values_base, values_combined=values_combined)

