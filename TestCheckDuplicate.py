import time
import datetime
#import mysql.connector
#import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import AuxFunctions
import TesteMissingElement




#url = 'https://www.sainsburys.co.uk/gol-ui/product/cerelac-mixed-fruits-wheat-fruits-bl%C3%A9-with-milk-from-7-months-400g'
#url = 'https://www.sainsburys.co.uk/gol-ui/product/ellas-kitchen-banana-poppy-seed-overnight-oats-with-apple-pieces-7-months-130g'
url = 'https://www.sainsburys.co.uk/gol-ui/groceries/baby-and-toddler/baby-milk-and-drinks/all-baby-milk-and-drinks/c:1018696'

button = '//*[@id="onetrust-accept-btn-handler"]'


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



def product_name(item, selector):
    
    try:
        return item.find(selector, title = True)['title']
    
    except TypeError:
        return None
    
    
def product_link(item, selector):
    
    try:
        return item.find(selector, href=True)['href']
    
    except TypeError:
        return None
    


def click(selector):
       
    try:
        driver.find_element(By.XPATH, selector).click()
            
    except NoSuchElementException:
        return False
    


driver.get(url)
time.sleep(3)

click(button)
time.sleep(3)
soup=BeautifulSoup(driver.page_source,'lxml')
data = soup.select("#root > div.app > div.ln-o-page > div.ln-o-page__body > div > div > div > section > ul > li")
for item in data:
    product_ID = 101010
    a = 10
    for item in data:
        product_data = {
                'date': datetime.date.today(),
                'product_ID': AuxFunctions.product_code(product_ID, a),
                'name': product_name(item, 'a'),
                'price': AuxFunctions.extract_data(item, 'span.pt__cost__retail-price'),
                'price_per': AuxFunctions.extract_data(item, 'span.pt__cost__unit-price-per-measure'),
                'nectar_price': AuxFunctions.extract_data(item, 'span.pt__cost--price'),
                'price_kg': AuxFunctions.extract_data(item, 'select'),
                'label': AuxFunctions.extract_data(item, 'div.pt__badges'),
                'product_link': product_link(item, 'a')
            }
        a+=1

        if product_data.get('price_kg') == None:
            print(product_data)

        

        else:
            link = product_data.get('product_link')
            product_ID = product_data.get('product_ID')
            TesteMissingElement.scrape_product_page(link, product_ID)

        




