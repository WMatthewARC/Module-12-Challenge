from flask import Flask, render_template
from flask_pymongo import PyMongo
import datetime
from scrape_mars import scrape

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# Mongo setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_data = mongo.db.mars_data.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def do_scrape():
    mars_data = scrape()

    mars_table = mongo.db.mars_data

    mars_table.drop()

    mars_table.insert_one(mars_data)

    return "Done", 200


if __name__ == '__main__':
    app.run(debug=True)
