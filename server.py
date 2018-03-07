import logging

from flask import Flask
from flask import render_template
from flask import request

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
    return render_template("home.html")

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
    return render_template("submitted.html")

@app.route("/query")
def get_query():
    """
    Get query from user and process it.
    Render HTML that will contain the plot.
    """
    return render_template("plot.html")
if __name__ == "__main__":
    app.run()
