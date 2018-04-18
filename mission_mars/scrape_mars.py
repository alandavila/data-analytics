# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:43:33 2018

@author: davil
"""
# Dependencies
from bs4 import BeautifulSoup
from flask import Flask, render_template
import pandas as pd
import pymongo
import requests
from splinter import Browser
import time

def scrape():
    mars_dict = {}
    #Scrape NASA Mars News
    #Set dict with chromedriver executable location
    executable_path = {'executable_path': 'C:\Program Files (x86)\ChromeDriver\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    #Mars exploration program web site
    url = 'https://mars.nasa.gov/'
    browser.visit(url)
    #Navigate to news page via -> New -> More News
    browser.click_link_by_partial_text('News')
    time.sleep(3)
    browser.click_link_by_partial_text('More News')
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #get all list items from the page
    results = soup.find_all('li', class_="slide")
    #collect the latest news title and paragraph
    news_title = results[0].find('div', class_='content_title').a.text
    news_p = results[0].find('div',class_='article_teaser_body').text
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p
    
    #JPL Mars Space Images - Featured Image
    #Navigate to site of NASA's featured images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #get all list items from the page
    results = soup.find_all('li', class_="slide")
    #collect the first features image
    featured_image_url = results[0].find('div', class_='img').img['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url
    mars_dict['featured_image_url'] = featured_image_url

    #Scrap Mars Weather
    #Navigate to the Mar's weather twitter account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #get last tweet
    tweet = soup.find('div', class_='js-tweet-text-container')
    mars_weather = tweet.p.text
    mars_dict['mars_weather'] = mars_weather

    #Scrap Mars Facts
    #read html tables form web site using pandas
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    mars_dict['html_table'] = html_table
    
    #Scrape Mars Hemisperes
    #Navigate to the astrogeology web site with "Mars" query
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #save all image titles and links in a list
    hemisphere_image_urls  = []
    descriptions = soup.find_all('div', class_='description')
    for description in descriptions:
        image_dict = {}
        title = description.a.h3.text
        image_dict['title'] = title
        #navigate to each image
        browser.click_link_by_partial_text(title)
        #find image element and get image link from src
        soup = BeautifulSoup(browser.html, 'html.parser')
        image_link = soup.find('img',class_='wide-image')
        image_link = 'https://astrogeology.usgs.gov' + image_link['src']
        image_dict['img_url'] = image_link
        hemisphere_image_urls.append(image_dict)
        #go back to navigate to next image
        browser.click_link_by_partial_text('Back')
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict


# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/scrape")
def web_scrape():
    
    #craete mongo database
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db 
    collection = db.mars_info
    #insert information scrapped form the web
    db.mars_info.insert_one(scrape())

# create route that renders index.html template
@app.route("/")
def show_data():
    
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db 
    collection = db.mars_info
    mars_dict = db.collection.find()

    return render_template(
        "index.html", 
        mars_dict=mars_dict
        )

if __name__ == "__main__":
    app.run(debug=True)














