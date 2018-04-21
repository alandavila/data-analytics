# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:43:33 2018

@author: davil
"""
# Dependencies
from flask import Flask, render_template,  url_for, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

#connect to mongo database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
#drop database if it exist to start fresh
client.drop_database('mars_db')
db = client.mars_db 
collection = db.mars_info
# create route that scraps new data
@app.route("/scrape")
def web_scrape():
    #insert information scrapped form the web
    scraped_info = scrape_mars.scrape()
    db.drop_collection('mars_info')
    collection.insert_one(scraped_info)
    mars_dict = collection.find()
    mars_dict = list(mars_dict)[0]
    return render_template(
        "index.html", mars_dict = mars_dict
        )

# create route that renders index.html template
@app.route("/")
def index():
    #if there is no data in db then use test dict to render page
    try:
        mars_dict = collection.find()
        mars_dict = list(mars_dict)[0]
    except:
        mars_dict = scrape_mars.scrape_test()
    
    return render_template(
        "index.html", 
            mars_dict = mars_dict
        )

if __name__ == "__main__":
    app.run(debug=True)














