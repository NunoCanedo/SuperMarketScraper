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



url='https://www.tesco.com/groceries/en-GB/shop/fresh-food/fresh-meat-and-poultry/fresh-beef?page=2'

# Define day of the date scraped
#day = datetime.date.today()    ##ADD again later(not been used for testing porpouse)
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

def name_price_weight(soup, selector):
    try:
        return soup.select_one(selector).text
    except AttributeError:
        return None


def product_info(url_info):
    for url_string in url_info:
        page = url_string.get('product_link')
        print(page)
        
        url = f'https://www.tesco.com{page}'   #https://www.tesco.com/groceries/en-GB/products/258139435
        print(url)
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'lxml')

        y = url.replace('https://www.tesco.com/groceries/en-GB/products/','')
        selector_1 = f'#catch-weight-{y} > option:nth-child(1)'
        selector_2 = f'#catch-weight-{y} > option:nth-child(2)'
        selector_3 = f'#catch-weight-{y} > option:nth-child(3)'
        selector_4 = f'#catch-weight-{y} > option:nth-child(4)'

        items = {
            'name': name_price_weight(soup, '#asparagus-root > div > div.template-wrapper > main > div > div > div.styled__PDPTileContainer-mfe-pdp__sc-ebmhjv-0.cEAseF.pdp-tile > div > section.styled__GridSection-mfe-pdp__sc-ebmhjv-1.bjEIyj > h1'),
            'weight_1': name_price_weight(soup, selector_1),
            'weight_2': name_price_weight(soup, selector_2),
            'weight_3': name_price_weight(soup, selector_3),
            'weight_4': name_price_weight(soup, selector_4)
            #'value': soup.find('option:nth-child(2)', value = True)['value']          
        }
        #whatever_1.append(items)

       
        print(items)
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
        'price_weight': extract_data(product, 'div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container> div > div'), ## May need de product number for specific cases
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
    ###tile-292606718 > div.product-details--wrapper > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container
    ##tile-258139435 > div.product-details--wrapper > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container
    ##tile-258139435 > div.product-details--wrapper > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container > label
    ##tile-258139435 > div.product-details--wrapper > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container > div
##tile-258139435 > div.product-details--wrapper > div.styles__StyledBuyBoxWrapper-dvv1wj-4.dSvjUC > div > div > form > div > div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container > div > div
##catchWeight-258139435

    #if products_list.get('price_weight') == None:
    #print(products_list)

    for item in products_list:
        print(item)

    print('====================================')

    product_info(products_to_scrape)
    
        
            

    #products = pd.DataFrame(products_list) 

    #products.to_csv('products_csv')
    


## Function to Parse the WebPage

def parser_url(url):

    #Parametres to scrape the Page
    #Needs to be worked out o be able to scrape without open a browser 

    

    ## Next parameters aren't needed but may be usefull
    #accept cookie
    #driver.find_element(By.XPATH,'//*[@id="onetrust-button-group-parent"]/div/button[1]').click()
    #time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'lxml')

    Product_data(soup)
    

parser_url(url)
    