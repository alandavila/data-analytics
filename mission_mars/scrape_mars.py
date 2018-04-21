# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:43:33 2018

@author: davil
"""
# Dependencies
from bs4 import BeautifulSoup
from selenium import webdriver
from splinter import Browser
import pandas as pd
import time
import os

def scrape_test():
    raw_html = r'<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Value</th>    </tr>    <tr>      <th>Description</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'
    mars_dict = {"_id":"5ad7fe01e9fd7b12e0fd3488",
                 "news_title":"Bound for Mars: Countdown to First Interplanetary Launch from California",
                 "news_p":"On May 5, millions of Californians may witness the historic first interplanetary launch from America’s West Coast.",
                 "featured_image_url":"https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA22372-640x350.jpg",
                 "mars_weather":"Sol 2024 (April 16, 2018), Sunny, high -7C/19F, low -76C/-104F, pressure at 7.20 hPa, daylight 05:26-17:21",
                 "mars_facts":raw_html,
                 "hemisphere_image_urls":[
                         {"title":"Cerberus Hemisphere Enhanced",
                          "img_url":"https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"},
                         {"title":"Schiaparelli Hemisphere Enhanced",
                          "img_url":"https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
                         {"title":"Syrtis Major Hemisphere Enhanced",
                          "img_url":"https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
                         {"title":"Valles Marineris Hemisphere Enhanced",
                          "img_url":"https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"}
                         ]
                 }
    return mars_dict

def scrape():
    mars_dict = {}
    #Scrape NASA Mars News
    #Set dict with chromedriver executable location 
    path_to_chromedriver = 'C:\Program Files (x86)\ChromeDriver\chromedriver.exe'
    executable_path = {'executable_path': path_to_chromedriver}
    browser = Browser('chrome', **executable_path, headless=False)
    #Mars exploration program web site
    url = 'https://mars.nasa.gov/'
    browser.visit(url)
    #Navigate to news page via -> New -> More News
    browser.click_link_by_partial_text('News')
    time.sleep(3)
    browser.click_link_by_partial_text('More News')
    time.sleep(10)
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #get all list items from the page
    results = soup.find_all('li', class_="slide")
    #collect the latest news title and paragraph
    news_title = results[0].find('div', class_='content_title').a.text
    news_p = results[0].find('div',class_='article_teaser_body').text
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p
    time.sleep(10)
    
    #JPL Mars Space Images - Featured Image
    #Navigate to site of NASA's featured images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #parse page
    soup = BeautifulSoup(browser.html, 'html.parser')
    #click on full image to get featured image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    #select image object
    soup = BeautifulSoup(browser.html, 'html.parser')
    results = soup.find('img', class_ = 'fancybox-image')
    #extract image url info
    featured_image_url = results['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url
    mars_dict['featured_image_url'] = featured_image_url
    time.sleep(10)
    
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

#    #Scrap Mars Facts
#    #read html tables form web site using pandas
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    mars_dict['mars_facts'] = html_table
    
    time.sleep(10)
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
