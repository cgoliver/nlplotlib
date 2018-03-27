import os
import sys
import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
import numpy as np

from plotter import make_plot
from nn import ea
from romanlp import get_action_from_sentence
from embedding import *
from logger import log_gen

app = Flask(__name__)
app.secret_key = 'some_secret'

#load word2vec model

w2v = model_load()

#get nerual net generator
nns = ea((50, 20, 20, 10))
next(nns)

log = log_gen()
next(log)

def parse_query(query):
    """
    Parse query into vector.
    """
    pass

def graph_gen(query, data):
    """
    i.   Pass query to parser.
    ii.  Pass parsed query to EA.
    iii. Create graph with EA prediction.

    Returns path to figure.
    """
    pass

def model_update(score):
    """
    Update EA with `score` from user.
    """
    pass

       
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
    if request.method == 'POST':
        result = request.form

        query = result['query']
        #if no filepath, use iris.csv. 
        #also need to check extension in case plot uploaded
        parsed = get_action_from_sentence(query)
        complements = parsed[1]
        embed = sentence_embed(w2v, complements)

        if not result['file']:
            datapath = 'static/iris.csv'
        else:
            datapath = result['file']

        #call NN
        # next(nns)
        #send query to ea, get prediction
        prediction = nns.send(embed)

        #use prediction to make plot
        plotname, time = make_plot(prediction, 1)

        log.send((query, parsed, embed, plotname))

        return render_template("submitted.html", plotname=plotname,\
            result=result, time=time)

@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        result = request.form['rating']
        logger.info(result)
        #send feedback to NN
        # next(nns)
        nns.send(float(result))

        log.send(result)
    return ('', 204)
    # return "Feedback recorded!"
if __name__ == "__main__":
    app.run()
