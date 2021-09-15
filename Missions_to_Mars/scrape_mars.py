# Import BeautifulSoup, Pandas, and Requests/Splinter.
from bs4 import BeautifulSoup
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    #-------------------------------
    #       NASA Mars News
    # ------------------------------
    # Setup splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    # collect the latest News Title and Paragraph Text
    news_title = soup.find('div',class_='content_title').get_text()
    news_p = soup.find('div',class_='article_teaser_body').get_text()
    browser.quit()

    #-------------------------------
    #       JPL Mars Space Images - Featured Image
    # ------------------------------
    # Setup splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    partial_image_url = soup.find('img',class_='fancybox-image')['src']
    featured_image_url = f"{url}{partial_image_url}"
    browser.quit()


    #-------------------------------
    #       Mars Facts
    # ------------------------------
    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(requests.get(url).text)
    fact_df = tables[0]
    new_header = fact_df.iloc[0]
    fact_df = fact_df[1:] 
    fact_df.columns = new_header 
    fact_df.set_index("Mars - Earth Comparison",inplace=True)
    html_table = fact_df.to_html().encode("ISO-8859-1").decode()


    #-------------------------------
    #       Mars Hemispheres
    # ------------------------------
    # Setup splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div',class_='item')
    links = []
    for item in items:
        link = f"{url}{item.a['href']}"
        links.append(link)  
    hemisphere_image_urls = []
    for link in links:
        info = {}
        #go to each page
        browser.visit(link)
        #start scraping
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
    
        title = soup.find('h2',class_ = 'title').text
        partial_img_url = soup.find('img',class_='wide-image')['src']
        img_url = f"{url}{partial_img_url}"
        info['title']=title
        info['img_url']=img_url
        hemisphere_image_urls.append(info)
        # go back to the main page
        browser.links.find_by_partial_text('Back').click()
    browser.quit()

    listings = {
        'news_title':news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_image_urls':hemisphere_image_urls
    }

    return listings