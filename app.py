from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_amitava

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    final_output = mongo.db.mars_data.find_one()
    return render_template("index.html", final_output=final_output)

@app.route("/scrape")
def scraper():
    mars_db = mongo.db.mars_data    
    mars_dict = scrape_mars_amitava.scrape()
    mars_db.update({}, mars_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
