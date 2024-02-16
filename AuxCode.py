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

# Define day of the date scraped
#day = datetime.date.today()    ##ADD again later(not been used for testing porpouse)


url='https://www.tesco.com/groceries/en-GB/shop/fresh-food/fresh-meat-and-poultry/fresh-chicken'



## Function to avoid errors when different data or unvalable data is displayed in the WebPage

def extract_data(product, selector):
    try:
        return product.select_one(selector).text
    except AttributeError:
        return None



## Function to loop and scrape data from each product

def Product_data(soup):

    products_list = []
    products_to_scrape = []

    html=soup.select_one('#product-list > div.product-list-view.has-trolley > div.product-list-container > div > div > div.category.product-list--page.product-list--current-page > div > ul')


    ## Loop the list of products in the page to get necessary data
    for product in html:
        items = {
        'name': extract_data(product, 'h3.styles__H3-oa5soe-0'),
        'price': extract_data(product, 'p.styled__StyledHeading-sc-119w3hf-2'),
        #This is for product were weight have to be selected
        'price_weight': extract_data(product, 'div.product-details--wrapper > div.styles__StyledPromotionsWithBuyBoxWrapper-dvv1wj-8.cZskDh > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container > div'), ## May need de product number for specific cases
        'Clubcard Price': extract_data(product, 'span.offer-text'),
        ##ADD again later(not been used for testing porpouse)
        #f'{day} - Clubcard Price': extract_data(product, 'span.offer-text'), ## still need to work this out
        'product_link': product.find('a', href=True)['href'],

        ## Scraping the origin in the page for a possible use to create ID's in a more organized way if needed
        'department': extract_data(soup, '#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(2)'),
        'category': extract_data(soup, '#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(3)'),
        'sub_category': extract_data(soup, '#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(4)')
        }
        if items.get('price_weight') == None:
            products_list.append(items)

        else:
            products_to_scrape.append(items)
    
    
    #if products_list.get('price_weight') == None:
    #print(products_list)

    for item in products_list:
        print(item)
        
            

    products = pd.DataFrame(products_list)
    list_to_scrape = pd.DataFrame(products_to_scrape) 

    products.to_csv('products_csv')
    list_to_scrape.to_csv('list_to_scrape_csv')
    


## Function to Parse the WebPage

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