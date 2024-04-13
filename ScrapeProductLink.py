## Import Libraries

import AuxFunctions
import SqlFunctions

#import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException




##Define Driver

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



## Function to click and change options for special case products

def change_options(selector):
    try:
        return driver.find_element(By.XPATH, selector).click()
    except NoSuchElementException:
        pass



## Function for pages were options need to be choosen 

def scrape_product_page(link, product_ID):
    print(link)
    print('______________________')
    driver.get(link)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'lxml')
    something = soup.find('#root > div.app > div.ln-o-page > div.ln-o-page__body > div > div > div > div > section:nth-child(2) > div > div > div.pd__right > div.pd__data-entry')
    
    if something == None:
        pass
    
    else:


        ## Function to find the diferent elements in the page
        def extract_info(selector):
            try:
                return driver.find_element(By.XPATH, selector).text
            except NoSuchElementException:
                pass


        ## Function to extract data inside product page
        def page_data(selector):
            try:
                return soup.select_one(selector).text
            except AttributeError:
                return None
        
        b = 1

        base_selector = soup.find('select', id=True)['id']
        selectors = [f'//*[@id="{base_selector}"]/option[1]',
                    f'//*[@id="{base_selector}"]/option[2]',
                    f'//*[@id="{base_selector}"]/option[3]',
                    f'//*[@id="{base_selector}"]/option[4]',
                    f'//*[@id="{base_selector}"]/option[5]']
        for selector in selectors:
            change_options(selector)
            
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source,'lxml')
            #weight = extract_info(selector)
            name  = page_data('h1.pd__header'), extract_info(selector)
            price = page_data('span.pd__cost__retail-price')
            #price_2 = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div/section[1]/div/div/div[2]/div[6]/div[1]/div/div[2]/span[2]').text
            price_per = page_data('span.pd__cost__unit-price-per-measure')
            nectar_price = page_data('span.pd__cost--price')
            product_data = {
                'date': datetime.date.today(),
                'product_ID': AuxFunctions.product_code(product_ID, b),
                'name': str((page_data('h1.pd__header'), extract_info(selector))).replace('("', '').replace("')", ''),
                'price': page_data('span.pd__cost__retail-price'),  
                'nectar_price': page_data('span.pd__cost--price'),
                'price_per': page_data('span.pd__cost__unit-price-per-measure'),
                'label': page_data('div.pd__shortmeta'),
                'product_link': link
            }

            b+=1

            #<div class="pd__shortmeta"><div class="pd__shortmeta__item"><div class="pd__label" aria-label="Chilled" style="border: 1px solid rgb(0, 80, 150); color: rgb(0, 80, 150);">Chilled</div></div><div class="pd__shortmeta__item"><a href="/shop/gb/groceries/get-ideas/delivery-and-guides/freshness" target="_self" rel="noreferrer"><div class="pd__label" aria-label="Typical life 7 days" style="border: 1px solid rgb(33, 130, 52); color: rgb(33, 130, 52);">Typical life 7 days</div></a></div></div>
            stop = extract_info(selector)
            
            if stop == None:
                pass
            
            else:
                product = []
                aux_product = []
                product.append(product_data)
                aux_product.append(product_data)
                
                

            
                SqlFunctions.insert_values(product, 'PriceDate')
                
                SqlFunctions.insert_values(aux_product, 'AuxTable')
                

