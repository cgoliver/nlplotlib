import os
import logging

from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import import secure_filename

app = Flask(__name__)

#logging stuff
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('nlplotlib.log')
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/query")
def get_query():
    """
    Get query from user and process it.
    Render HTML that will contain the plot.
    """
    #change this to take variable path
    return render_template("plot.html")
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#check this out: http://pythonhosted.org/Flask-Uploads/
@app.route("/submitted", methods=['GET', 'POST'])
def process_request():
    """
    Process user query and data file.
    """

    #save file
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    if file.filenmae == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    #process query
    query = request['query']
    #return plot HTML
    return '''hello '''
if __name__ == "__main__":
    app.run()
