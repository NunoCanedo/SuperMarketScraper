##Tesco search data

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import csv
import pandas as pd


day = datetime.date.today()

products_list = []
url='https://www.tesco.com/groceries/en-GB/shop/christmas/christmas-dinner/finest-christmas-mains'


def Product_data(soup):
    html=soup.select_one('#product-list > div.product-list-view.has-trolley > div.product-list-container > div > div > div.category.product-list--page.product-list--current-page > div > ul')


    ## Scraping the origin in the page for a possible use to create ID's in a more organized way if needed

    department = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(2)')
    category = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(3)')
    sub_category = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(4)')
    

    ## Loop the list of products in the page to get necessary data
    for product in html:
        items = {
        'name': product.find('h3', class_='styles__H3-oa5soe-0').text,
        'price': product.find('div', data=True)['data-auto-id'],
        f'{day} - Clubcard Price': product.find('span', {'class': 'offer-text'}),
        'product_link': product.find('a', href=True)['href'],
        'department': department.text,
        'category': category.text,
        'sub_category': sub_category.text
        }
        products_list.append(items)

    products = pd.DataFrame(products_list)

    products.to_csv('products_csv')



def parser_url(url):

    #Parametres to scrape the Page
    #Needs to be worked out o be able to scrape without open a browser 

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")

    ## Don't need a path, next argument make automation to install if missing
    #webdriver_service = Service("./chromedriver") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)

    ## Next parameters aren't needed but may be usefull
    #accept cookie
    #driver.find_element(By.XPATH,'//*[@id="onetrust-button-group-parent"]/div/button[1]').click()
    #time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'lxml')

    Product_data(soup)
    

parser_url(url)
    
