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

    #time.sleep(1)
    browser.is_element_visible_by_css("#news")

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the Mars News site for the first article's title and description
    news_title = soup.select("#news .content_title")[0].text
    news_description = soup.select("#news .article_teaser_body")[0].text

    # Visit Mars Images site
    mars_images_url = 'https://spaceimages-mars.com/'
    browser.visit(mars_images_url)

    #time.sleep(1)
    browser.is_element_visible_by_css("img.headerimage")

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the featured image and grab the url
    image = soup.select("img.headerimage")[0]
    featured_image_url = mars_images_url + image['src']

    # Close browser
    browser.quit()

    # Scrape the Mars Facts using Pandas
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    facts_tables = pd.read_html(mars_facts_url)
    facts_tables[0].columns=["Description", "Mars", "Earth"]

    # Grab the facts table as HTML
    mars_facts_html = facts_tables[0].to_html(classes="table", header=None, index=False)
    
    # Store High res images
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
        {"title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"},
    ]

    result = {
        "news_title": news_title,
        "news_summary": news_description,
        "featured_image_url": featured_image_url,
        "facts_table_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return result