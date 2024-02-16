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
import re
from csv import DictReader


day = datetime.date.today()

products_list = []
#url='https://www.tesco.com/groceries/en-GB/products/268880572'
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")

    ## Don't need a path, next argument make automation to install if missing
    #webdriver_service = Service("./chromedriver") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get(url)
#driver.maximize_window()
#time.sleep(5)

#driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]').click()
#time.sleep(3)
#driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[1]').click()
#time.sleep(3)
#price = soup.select_one('#asparagus-root > div > div.template-wrapper > main > div > div > div.styled__PDPTileContainer-mfe-pdp__sc-ebmhjv-0.cEAseF.pdp-tile > div > section.styled__GridSection-mfe-pdp__sc-ebmhjv-1.bjEIyj > div.styled__Details-mfe-pdp__sc-ebmhjv-7.dqYwFc > div.styled__BuyBoxContainer-mfe-pdp__sc-ebmhjv-5.hkkbie > div > div.base-components__BaseElement-sc-150pv2j-0.styled__PriceAndActions-sc-159tobh-3.chGOgR.bgcAqA.ddsweb-buybox__price-and-actions > div.base-components__RootElement-sc-150pv2j-1.styled__Container-sc-v0qv7n-0.hjMZDF.gVxPxM.styled__StyledPrice-sc-159tobh-5.grMosf.ddsweb-buybox__price.ddsweb-price__container > p.styled__StyledHeading-sc-1a9r96t-2.gSatyL.styled__Text-sc-v0qv7n-1.ecTMDe').text
def name_price_weight(soup, selector):
    try:
        return soup.select_one(selector).text
    except AttributeError:
        return None



whatever_1 = []

links_to_scrape = open('list_to_scrape_csv', 'r')
url_info = DictReader(links_to_scrape)

def product_info(url_info):
    for url_string in url_info:
        page = url_string.get('product_link')
        
        url = f'https://www.tesco.com{page}'   #/groceries/en-GB/products/268880284
        print(url)
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'lxml')

        y = url.replace('https://www.tesco.com/groceries/en-GB/products/','')
        selector_1 = f'#catch-weight-{y} > option:nth-child(1)'
        selector_2 = f'#catch-weight-{y} > option:nth-child(2)'
        selector_3 = f'#catch-weight-{y} > option:nth-child(3)'
        selector_4 = f'#catch-weight-{y} > option:nth-child(4)'
        #//*[@id="catch-weight-275492600"]/option[1]

        items = {
            'name': name_price_weight(soup, '#asparagus-root > div > div.template-wrapper > main > div > div > div.styled__PDPTileContainer-mfe-pdp__sc-ebmhjv-0.cEAseF.pdp-tile > div > section.styled__GridSection-mfe-pdp__sc-ebmhjv-1.bjEIyj > h1'),
            'weight_1': name_price_weight(soup, selector_1),
            'weight_2': name_price_weight(soup, selector_2),
            'weight_3': name_price_weight(soup, selector_3),
            'weight_4': name_price_weight(soup, selector_4)
            #'value': soup.find('option:nth-child(2)', value = True)['value']          
        }
        whatever_1.append(items)

       
        print(items)

        df = pd.DataFrame(whatever_1)

        df.to_csv('items.csv')
        
       



#<option class="ddsweb-buybox__option" value="1.68">1.68kg/£20.16</option>
#<option class="ddsweb-buybox__option" value="1.68">1.68kg/£20.16</option>
#<option class="ddsweb-buybox__option" value="3">3kg/£36.00</option>
#<option selected="" class="ddsweb-buybox__option" value="2.34">2.34kg/£28.08</option>
##catch-weight-268880572 > option:nth-child(2)


if __name__ == '__main__':
    product_info(url_info)
##catch-weight-268880572 > option:nth-child(2)
#print(weight_4)


#driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[2]').click()
#time.sleep(3)
#driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[3]').click()
#time.sleep(3)
#driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[4]').click()
#time.sleep(3)

#<p class="styled__StyledHeading-sc-1a9r96t-2 gSatyL styled__Text-sc-v0qv7n-1 ecTMDe">£25.50</p>
##asparagus-root > div > div.template-wrapper > main > div > div > div.styled__PDPTileContainer-mfe-pdp__sc-ebmhjv-0.cEAseF.pdp-tile > div > section.styled__GridSection-mfe-pdp__sc-ebmhjv-1.bjEIyj > div.styled__Details-mfe-pdp__sc-ebmhjv-7.dqYwFc > div.styled__BuyBoxContainer-mfe-pdp__sc-ebmhjv-5.hkkbie > div > div.base-components__BaseElement-sc-150pv2j-0.styled__PriceAndActions-sc-159tobh-3.chGOgR.bgcAqA.ddsweb-buybox__price-and-actions > div.base-components__RootElement-sc-150pv2j-1.styled__Container-sc-v0qv7n-0.hjMZDF.gVxPxM.styled__StyledPrice-sc-159tobh-5.grMosf.ddsweb-buybox__price.ddsweb-price__container > p.styled__StyledHeading-sc-1a9r96t-2.gSatyL.styled__Text-sc-v0qv7n-1.ecTMDe