import os
import shutil
import sys
import logging
import uuid

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
# from romanlp import get_action_from_sentence
# from embedding import *
from logger import log_gen

# logging.basicConfig(filename='main.log',level=logging.DEBUG)

UPLOAD_FOLDER = '/Users/carlosgonzalezoliver/Projects/NLPlotlib/static/plots'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


        if 'file' not in request.files:
            datapath = 'static/iris.csv'
            plot_id = str(uuid.uuid1())
            print(plot_id)
        else:
            pass
            f = request.files['file']
            print(f)
            filename = f.filename
            s_filename = secure_filename(filename)
            #check if existing plot
            file_id = filename.split(".")[0]
            file_exists = file_id in os.listdir(app.config['UPLOAD_FOLDER'])
            if filename.endswith(".pickle"):
                if file_exists:
                    filedir = file_id
                else:
                    return "DID NOT FIND THAT PLOT IN OUR DATABASE"
            else:
                filedir = str(uuid.uuid1())

            try:
                savepath = os.path.join(app.config['UPLOAD_FOLDER'],\
                    filedir)
                os.makedirs(savepath)
                print(savepath)
                f.save(os.path.join(savepath, s_filename))
            except Exception as e:
                print(e)
                return "SAVING ERROR TRY AGAIN"

        #send query to ea, get prediction
        prediction = nns.send(embed)

        #use prediction to make plot
        plotname, time = make_plot(1, 1)

        plotpath = os.path.join('static', 'plots', plotname)
        #make zip of plot folder
        shutil.make_archive(plotpath , 'zip', plotpath)

        log.send((query, parsed, embed, plotname))

        return render_template("submitted.html", plotname=plotname,\
            result=result, time=time)

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
