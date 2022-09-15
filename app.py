from flask import Flask, jsonify
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

@app.route("/scrape")
def do_scrape():
    mars_data = scrape()

    mars_table = mongo.db.mars_data

    mars_table.drop()

    mars_table.insert_one(mars_data)

    return "Done", 200


if __name__ == '__main__':
    app.run(debug=True)
