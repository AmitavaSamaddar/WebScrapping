#Python file created using the commands from jupyter notebook file
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

executable_path = {'executable_path': 'drivers/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():

    #URLs -

    base_url = 'https://mars.nasa.gov/news/'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    img_url_base = 'https://www.jpl.nasa.gov'
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = 'http://space-facts.com/mars/'
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Visiting main page
    browser.visit(base_url)
    time.sleep(2)
    html = browser.html

    #Getting data
    soup = BeautifulSoup(html, "html.parser")

    #Getting the 1st title
    title = soup.find('div', class_='content_title')
    news_title = title.text
    
    #Getting paragraph text from 1st title
    para = soup.find('div', class_='article_teaser_body')
    news_p = para.text

    #Visiting URL to get the image
    browser.visit(img_url)
    #Clicking on 'Full Image'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)

    #Clicking on 'More Info'
    browser.click_link_by_partial_text('more info')
    time.sleep(1)

    #Getting data
    soup = BeautifulSoup(browser.html, "html.parser")
    #Image data
    image = soup.find('img', class_='main_image')
    #Image URL
    featured_image_url = img_url_base + image["src"]

    #Getting data from Twitter page
    browser.visit(twitter_url)
    soup = BeautifulSoup(browser.html, "html.parser")

    #Getting the tweet
    tweet = soup.find('p', class_='tweet-text')
    mars_weather = tweet.text

    #Getting Mars Facts
    facts = pd.read_html(facts_url)
    df_facts = facts[0]
    df_facts.columns = ["Items", "Values"]

    #Creating HTML Table
    facts_html = df_facts.to_html()
    facts_html = facts_html.replace('\n', '')
    
    #Getting Hemisphere details
    #Create empty bucket
    hemisphere_image_urls = []
    #Visiting the site and getting data using BeautifulSoup
    browser.visit(hemi_url)
    soup = BeautifulSoup(browser.html, 'lxml')
    #Fetching all items
    items = soup.find_all(class_='item')

    for item in items:
        browser.visit(hemi_url)
        browser.click_link_by_partial_text(item.h3.text)
        soup = BeautifulSoup(browser.html, 'lxml')
        
        title = item.h3.text.replace(' Enhanced', '')
        img_url = soup.find(target='_blank')['href']
        
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
        
    browser.quit()

    #Output dictionary
    final_output = dict (
        news_title = news_title,
        news_para = news_p,
        f_image_url = featured_image_url,
        weather = mars_weather,
        facts = facts_html,
        hemi_images = hemisphere_image_urls
           )
    
    return final_output

