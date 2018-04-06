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
from flask import session
from werkzeug.utils import secure_filename
import numpy as np

from plotter import make_plot
from nn import * 
from nn import ea
from romanlp import get_action_from_sentence
from embedding import *
from logger import log_gen
import roman_wrappers
from roman_wrappers import *
from conf import upload_folder
from conf import secret_key

# logging.basicConfig(filename='main.log',level=logging.DEBUG)

UPLOAD_FOLDER = upload_folder

app = Flask(__name__)
app.secret_key = secret_key

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#load word2vec model

glove = model_load()
SO = model_load("Data/model_SO_w2v_15d.word2vec")

embed_models= {"glove": (glove, "static/ea_glove.pickle"), "SO": (SO,\
    "static/ea_SO.pickle")}


#number of wrappers
num_wrappers = len([f for f in dir(roman_wrappers) if f.startswith('yy_')])

#get nerual net generator
# nns_glove = ea((50, 20, 20, num_wrappers), popsize=20)
# nns_SO = ea((15, 30, 30, num_wrappers), popsize=20)
# nns_list = (nns_glove, nns_SO)

#initialize neural nets
# for nns in nns_list:
    # next(nns)

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

        session['sess_id'] = str(uuid.uuid1())
        session['new_plot'] = False

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

            print("USING DEFAULT DATA")
            datapath = 'static/iris.csv'
            shutil.copyfile(datapath, os.path.join(plot_dir, "data.csv"))

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
            embed = None
            embed_choice = None
            session['new_plot'] = True 
            try:
                xx_draw_plot(actions, values, plot_id) 
            except:
                return "oops failed to make plot"

        else:
            #modifying plot
            parsed = get_action_from_sentence(query)
            actions, values = parsed
            print(f"actions: {actions}, values: {values}")
            embed_choice = random.choice(list(embed_models.keys()))
            emb, nn = embed_models[embed_choice]

            embed = sentence_embed(emb, actions)

            prediction, nn_ind = query_predict(embed, nn)

            session['nn'] = True
            session['nn_ind'] = nn_ind
            session['embedding'] = embed_choice

            print(prediction)
            #use prediction to make plot
            try:
                make_plot(prediction, actions, values, plot_id)
            #if wrapper fails, keep old plot
            except:
                pass 

        #make zip of plot folder
        shutil.make_archive(plot_dir, 'zip', plot_dir)

        # log.send((query, parsed, embed, plotname))
        job_info = (query, parsed, embed, plot_id, embed_choice)
        state_dump('static/training.pickle', session['sess_id'], job_info)

        return render_template("submitted.html", plotname=plot_id,\
            result=result, plotid=plot_id)

@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    print("reached")
    # logging.info("REACHED")
    if request.method == 'POST':
        result = request.form['rating']
        if session['new_plot']:
            state_dump("static/training.pickle", session['sess_id'], result)
        else:
            pickle_path = embed_models[session['embedding']][1]
            mean, std= update_EA(float(result), session['nn_ind'],pickle_path)
            state_dump("static/training.pickle", session['sess_id'], (result, mean, std))
    return ('', 204)

def state_dump(pickle_path, sess_id, data_list):
    state_dict = pickle.load(open(pickle_path, "rb"))
    state_dict.setdefault(sess_id, []).append(data_list)
    pickle.dump(state_dict, open(pickle_path, "wb"))
if __name__ == "__main__":
    app.run(debug=True)
