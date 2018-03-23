import os
import logging

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from plotter import make_plot
from nn import ea

app = Flask(__name__)

#logging stuff
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('nlplotlib.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

nns = ea()

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
        # q = parse_query(result['query'])
        #if no filepath, use iris.csv. 
        #also need to check extension in case plot uploaded
        if not result['file']:
            datapath = 'static/iris.csv'
        else:
            datapath = result['file']

        #call NN
        next(ea)
        #send query to ea, get prediction
        prediction = ea.send([1, 2])

        #use prediction to make plot
        plotname, time = make_plot(1, 1)

        return render_template("submitted.html", plotname=plotname,\
            result=result, time=time)

@app.route("/feedback", methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        result = request.form['rating']
        logger.info(result)
        #send feedback to NN
        next(ea)
        ea.send(float(result))
    return "Feedback recorded!"
if __name__ == "__main__":
    app.run()