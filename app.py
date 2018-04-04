import os
import shutil
import sys
import logging
import uuid

import pandas as pd
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
from roman_wrappers import *

# logging.basicConfig(filename='main.log',level=logging.DEBUG)

UPLOAD_FOLDER = '/Users/carlosgonzalezoliver/Projects/NLPlotlib/static/plots'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#load word2vec model

# w2v = model_load()

#get nerual net generator
nns = ea((50, 20, 20, 10), popsize=20)
next(nns)

log = log_gen()
next(log)

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
        # parsed = get_action_from_sentence(query)
        # complements = parsed[1]
        # embed = sentence_embed(w2v, complements)
        parsed = ['bla', 'blo']
        actions = ["draw", "scatter", "plot"]
        values = ("grades.csv",["Test2","Final"])
        plot_id = "AA"
        complements = ['comp', 'blo']
        embed = np.zeros((50))


        new_plot = False
        plot_id = result['plotid'].replace(' ', '')
        plot_dir = None
        if plot_id:
            print(f"working on plot {plot_id}")
            if plot_id.strip() not in os.listdir(app.config['UPLOAD_FOLDER']):
                return "YOUR PLOT WAS NOT FOUND"
            else:
                print("MODIFYING EXISTING PLOT")
                plot_dir = os.path.join(app.config['UPLOAD_FOLDER'], plot_id)
        else:
            #need to create new plot folder
            plot_id = str(uuid.uuid1())
            plot_dir = os.path.join(app.config['UPLOAD_FOLDER'], plot_id)
            os.makedirs(plot_dir)
            new_plot = True
            f = request.files['file']
            #using default dataset
            if f.filename == '':
                print("USING DEFAULT DATA")
                datapath = 'static/iris.csv'
                shutil.copyfile(datapath, os.path.join(plot_dir, "data.csv"))
            #using uploaded dataset
            else:
                print("SAVING YOUR DATA")
                filename = f.filename
                # s_filename = secure_filename(filename)
                try:
                    f.save(os.path.join(plot_dir, "data.csv"))
                except Exception as e:
                    return "ERROR SAVING FILE"

        print(plot_dir)
        #extract column names from datafile
        df = pd.read_csv(os.path.join(plot_dir, "data.csv"))
        colnames = list(df.columns)

        #parser output: (['Draw','scatter', 'plot', 'testcsv'], [])
        if new_plot:
            print(query)
            print(f"server columns: {colnames}")
            parsed = get_action_from_sentence(query, columns=colnames)
            actions, values = parsed
            print("CALLING DRAW PLOT")
            xx_draw_plot(actions, values, plot_id) 
        else:
            parsed = get_action_from_sentence(query)
            actions, values = parsed
            yy_add_title(actions, values, plot_id)
           # call NN to plot 
        #send query to ea, get prediction
        # prediction = nns.send(embed)

        #use prediction to make plot
        # plotname, time = make_plot(1, 1)

        #make zip of plot folder
        shutil.make_archive(plot_dir, 'zip', plot_dir)

        # log.send((query, parsed, embed, plotname))

        return render_template("submitted.html", plotname=plot_id,\
            result=result, plotid=plot_id)

@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    print("reached")
    # logging.info("REACHED")
    if request.method == 'POST':
        result = request.form['rating']
        #send feedback to NN
        next(nns)
        stats = nns.send(float(result))
        next(nns)
        log.send((result, stats))
    return ('', 204)
    # return "Feedback recorded!"
    # return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=True)
