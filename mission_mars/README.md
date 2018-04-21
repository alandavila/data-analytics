

```python
# Dependencies
from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
import time
```

### NASA Mars News


```python
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
```


```python
#parse page
soup = BeautifulSoup(browser.html, 'html.parser')
#get all list items from the page
results = soup.find_all('li', class_="slide")
#collect the latest news title and paragraph
news_title = results[0].find('div', class_='content_title').a.text
news_p = results[0].find('div',class_='article_teaser_body').text
```

### JPL Mars Space Images - Featured Image


```python
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
featured_image_url
```




    'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA22374-640x350.jpg'



### Mars Weather


```python
#Navigate to the Mar's weather twitter account
url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)
#parse page
soup = BeautifulSoup(browser.html, 'html.parser')
#get last tweet
tweet = soup.find('div', class_='js-tweet-text-container')
mars_weather = tweet.p.text
```

### Mars Facts


```python
#read html tables form web site using pandas
url = 'https://space-facts.com/mars/'
table = pd.read_html(url)
```


```python
mars_df = table[0]
mars_df.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
  </tbody>
</table>
</div>




```python
mars_df.columns = ['Description', 'Value']
mars_df.set_index('Description', inplace=True)
mars_df.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Value</th>
    </tr>
    <tr>
      <th>Description</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
  </tbody>
</table>
</div>




```python
html_table = mars_df.to_html()
html_table.replace('\n', '')
```




    '<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th>Value</th>    </tr>    <tr>      <th>Description</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'



### Mars Hemisperes


```python
#Navigate to the astrogeology web site with "Mars" query
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
```


```python
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
```


```python
hemisphere_image_urls
```




    [{'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]
