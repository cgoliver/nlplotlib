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
import roman_wrappers
from roman_wrappers import *

# logging.basicConfig(filename='main.log',level=logging.DEBUG)

UPLOAD_FOLDER = '/Users/carlosgonzalezoliver/Projects/NLPlotlib/static/plots'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#load word2vec model

glove = model_load()
SO = model_load("Data/model_SO_w2v_15d.word2vec")

embeddings = (glove, SO)

#number of wrappers
num_wrappers = len([f for f in dir(roman_wrappers) if f.startswith('yy_')])

#get nerual net generator
nns_glove = ea((50, 20, 20, num_wrappers), popsize=20)
nns_SO = ea((15, 30, 30, num_wrappers), popsize=20)
nns_list = (nns_glove, nns_SO)

#call count
call_count = 0

#initialize neural nets
for nns in nns_list:
    next(nns)

log = log_gen()
next(log)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
    # call_count += 1
    if request.method == 'POST':
        result = request.form

        query = result['query']

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
            try:
                xx_draw_plot(actions, values, plot_id) 
            except:
                return "oops failed to make plot"
        else:
            #modifying plot
            parsed = get_action_from_sentence(query)
            actions, values = parsed
            try:
                embed = sentence_embed(embeddings[call_count%num_wrappers], actions)
            except:
                embed = np.zeros((50))
            #send query to ea, get prediction
            prediction = nns_list[call_count % num_wrappers].send(embed)
            print(prediction)
            # call NN to plot 
            # yy_add_title(actions, values, plot_id)
            #use prediction to make plot
            plotname, time = make_plot(prediction, actions, values, plot_id)

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
        cur_nn = nns_list[call_count % num_wrappers]
        next(cur_nn)
        stats = cur_nn.send(float(result))
        next(cur_nn)
        # log.send((result, stats))
    return ('', 204)
    # return "Feedback recorded!"
    # return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=True)
