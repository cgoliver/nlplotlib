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

@app.route("/")
def home():
    return render_template("home.html")
if __name__ == "__main__":
    app.run()
