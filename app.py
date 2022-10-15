"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from Scrapper import scrap_all, all_course
from mongodb import mongodbconnection
import logging


# Setting up logfile
logging.basicConfig(filename = 'flask_logs.log', format = '%(asctime)s %(message)s', filemode = 'w', level = logging.INFO)

# MongoDB connection using mongo connection module
databaseName = 'iNeuron_ReviewScrapper'
collectionName = 'course_collection'
dbcon = mongodbconnection(username = 'mongodb', password= 'mongodb')
ineuronCollection = dbcon.getCollection(dbName = 'iNeuron_ReviewScrapper', collectionName = 'course_collection')

# Function which automatically scraps all course data and saves to MongoDB server
try:
    scraps = scrap_all()
    logging.info('Scrap Successful')
except Exception as e:
    logging.error('Error in scrapping check Scrapper.py', e)


# Connect to Flask
app = Flask(__name__)
CORS(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    """Route to render the homepage"""
    course_in = all_course()
    logging.info("List of Course names Generated")
    return render_template("index.html", course_in = course_in)


@app.route('/course', methods = ['POST','GET'])
@cross_origin()
def result():
    """Route to render Results"""
    if request.method == 'POST':
        inputCourse = request.form['content'].replace("  "," ")
        course_data = ineuronCollection.find_one({"Course_title": inputCourse}, {"_id": 0})
        logging.info("User input is taken and result is generated")
        return render_template("result.html", course_data = course_data)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()