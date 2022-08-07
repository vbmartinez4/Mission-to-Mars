#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[3]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the NASA Mars News site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


# Parse the HTML
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit the Jet Propulsion Lab URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[12]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[15]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description',inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[78]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[79]:


# Parse the html with BeautifulSoup
html = browser.html
hemisphere_soup = soup(html, 'html.parser')
#hemisphere_soup

# Obtain all items for hemisphere information.
hemisphere_info = hemisphere_soup.find_all('div', class_='item')


# In[80]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[64]:


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


# In[82]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[83]:


# 5. Quit the browser
browser.quit()


# In[ ]:




