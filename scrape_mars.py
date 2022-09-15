from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # Set up driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars News
    mars_news_url = 'https://redplanetscience.com/'
    browser.visit(mars_news_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the Mars News site for the first article's title and description
    news_title = soup.select("#news .content_title")[0].text
    news_description = soup.select("#news .article_teaser_body")[0].text

    # Visit Mars Images site
    mars_images_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_images_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the featured image and grab the url
    image = soup.select("img.headerimage")[0]
    featured_image_url = image['src']

    # Close browser
    browser.quit()

    # Store Mars Facts HTML (scraped by Pandas)
    mars_facts_html = '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Description</th>\n      <th>Mars</th>\n      <th>Earth</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>Mars - Earth Comparison</td>\n      <td>Mars</td>\n      <td>Earth</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>Diameter:</td>\n      <td>6,779 km</td>\n      <td>12,742 km</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>Mass:</td>\n      <td>6.39 × 10^23 kg</td>\n      <td>5.97 × 10^24 kg</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>Moons:</td>\n      <td>2</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>Distance from Sun:</td>\n      <td>227,943,824 km</td>\n      <td>149,598,262 km</td>\n    </tr>\n    <tr>\n      <th>5</th>\n      <td>Length of Year:</td>\n      <td>687 Earth days</td>\n      <td>365.24 days</td>\n    </tr>\n    <tr>\n      <th>6</th>\n      <td>Temperature:</td>\n      <td>-87 to -5 °C</td>\n      <td>-88 to 58°C</td>\n    </tr>\n  </tbody>\n</table>'

    # Store High res images
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/cerberus_enhanced.tif"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced.tif"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced.tif"},
        {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced.tif"},
    ]

    result = {
        "News Title": news_title,
        "News Description": news_description,
        "Featured Image URL": featured_image_url,
        "Facts HTML": mars_facts_html,
        "Image URLs": hemisphere_image_urls
    }

    return result