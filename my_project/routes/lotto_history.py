from my_project import app
from flask import render_template
from my_project import db
from my_project.models import Winner, Lotto



@app.route("/lottery")

def staker_page():

    lottos = Lotto.query.all()

    winners = Winner.query.all()

    return render_template("lotto_history.html", page_title="Lotto Winner", lottos=lottos, winners=winners)
