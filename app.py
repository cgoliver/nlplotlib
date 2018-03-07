import os
import logging

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

app = Flask(__name__)

#logging stuff
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('nlplotlib.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

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
    """
    pass

def model_update(score):
    """
    Update EA with `score` from user.
    """
    pass

@app.route("/")
def home():
    x = 4
    return render_template("home.html")

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
    if request.method == 'POST':
        result = request.form
        
        return render_template("submitted.html", result=result)

if __name__ == "__main__":
    app.run()
