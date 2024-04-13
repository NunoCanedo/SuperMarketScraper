## Import Libraries

import SqlFunctions
import AuxFunctions
import ScrapeProductLink

import time
import datetime
import mysql.connector
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By






driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


url = SqlFunctions.url('Sainsburys_Taxonomy')


## Function to accept cokkies

def click(selector):
       
    try:
        driver.find_element(By.XPATH, selector).click()
            
    except NoSuchElementException:
        return False


   

## Function to look if there's more then then on page for each AISLE/SHLEVE 

def next_page(url, soup):
    try:
        soup=BeautifulSoup(driver.page_source,'lxml')
        page = soup.find('a', rel='next')
        next_page = ((page['href']).replace('#', ''))
    
        return url + '/opt/page:' + next_page

    except TypeError:
        return None


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

## Function to loop and get the data from all products on the page
    
def find_data(data, url):

    a = 10
    for item in data:
        product_data = {
                'date': datetime.date.today(),
                'product_ID': AuxFunctions.product_code(SqlFunctions.SQL_connection(url), a),
                'name': product_name(item, 'a'),
                'price': AuxFunctions.extract_data(item, 'span.pt__cost__retail-price'),
                'price_per': AuxFunctions.extract_data(item, 'span.pt__cost__unit-price-per-measure'),
                'nectar_price': AuxFunctions.extract_data(item, 'span.pt__cost--price'),
                'price_kg': AuxFunctions.extract_data(item, 'select'),
                'label': AuxFunctions.extract_data(item, 'div.pt__badges'),
                'product_link': product_link(item, 'a')
            }
            # Condiction to save the data from each product if no special conditions are needed
        if product_data.get('price_kg') == None:
                product = []
                product.append(product_data)

        
                SqlFunctions.insert_values(product, 'PriceDate')
                #product_csv = pd.DataFrame([product_data])
                #product_csv.to_csv('product_csv')
                #

            # Condiction to scrape special cases by product main Page
        else:
            link = product_data.get('product_link')
            product_ID = product_data.get('product_ID')
            ScrapeProductLink.scrape_product_page(link, product_ID)

        a+=1



## Function to GET URL ID from SQL DataBase

def get_ID(table_name):

    # Open the DataBase to collect the data (web_page_ID)

    db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '1001',
            database = 'SuperMarketScraper'
        )

    table_name = 'Sainsburys_Taxonomy'
    taxonomy = pd.read_sql('SELECT * FROM ' + table_name, db)

    cursor = db.cursor()
    query = 'SELECT ID FROM ' + table_name + ' WHERE web_page_ID = %s' 


    # Define only usefull web_page_ID's (WEB PAGE with ALL products are not scraped in this element) OBS: ALL will create duplicates so I'm not using those pages

    usefull_id = taxonomy.loc[~taxonomy['aisle'].str.contains('All'), ['ID', 'web_page_ID']]

    #ids = [1020328, 1020006] ------ > teste code


    ## Loop through all pages from SQL DataBase

    #for url in ids: ----- > teste code

    for url in usefull_id['web_page_ID']:
        
        #print(url)
        #x = [url]

        ## f string to create web adress with the ID from SQL DataBase

        page = f'https://www.sainsburys.co.uk/gol-ui/groceries/meat-and-fish/beef/beef-roasting-joints/c:{url}'
        
        print(page)

        driver.get(page)
        time.sleep(3)

        ## Click to accept cookies
        click('//*[@id="onetrust-accept-btn-handler"]')

        # Define soup and parse 
        soup=BeautifulSoup(driver.page_source,'lxml')
        data = soup.select("#root > div.app > div.ln-o-page > div.ln-o-page__body > div > div > div > section > ul > li")
        while next_page(page, soup) != None:

            aux_url = next_page(page, soup)
            driver.get(aux_url)
            time.sleep(3)
            soup=BeautifulSoup(driver.page_source,'lxml')
            data_2 = soup.select("#root > div.app > div.ln-o-page > div.ln-o-page__body > div > div > div > section > ul > li")
            find_data(data_2, url)
            print('£££££££')
            
            
        else:
            find_data(data, url)
            print('==========')
            
            




if __name__ == "__main__":
    get_ID('Sainsburys_Taxonomy')