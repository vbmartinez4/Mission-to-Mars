# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# ### The News: Titles and Summaries
def mars_news(browser):

    # Scrape Mars News
    # Visit the NASA Mars News site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Parse the HTML. Conver the browser html to a soup object and then quit the browser.
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Image
def featured_image(browser):

    # Visit the Jet Propulsion Lab URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ### Mars Facts
def mars_facts():
    try:
        # Use 'read_html' to scrape the facts table into a DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of DataFrame
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description',inplace=True)

    # Conver the DataFrame into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
def hemisphere(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Parse the html with BeautifulSoup
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    #hemisphere_soup

    # Obtain all items for hemisphere information.
    hemisphere_info = hemisphere_soup.find_all('div', class_='item')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Create loop to scrape through all hemisphere information
    for x in hemisphere_info:
        hemisphere = {}
    
        # Find the image title
        img_titles = x.find('h3').text
    
        # create link for full image
        link_ref = x.find('a', class_='itemLink product-item')['href']
        # Use the base URL to create an absolute URL and browser visit
        browser.visit(url + link_ref)
    
        # Find the image url
        img_html = browser.html
        hemis_soup = soup(img_html, 'html.parser')
        download = hemis_soup.find('div', class_= 'downloads')
        img_url = download.find('a')['href']
    
        # Add the img_url and title keys to the dictionary
        hemisphere['img_url'] = url + img_url
        hemisphere['title'] = img_titles
        hemisphere_image_urls.append(hemisphere)
    
        #Navigate back to the beginning to obtain next hemisphere image
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())