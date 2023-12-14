import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

product_list = []

def scrape(url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("detach", True)
    

    webdriver_service = Service("./chromedriver") #Your chromedriver path
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.maximize_window()
    time.sleep(1)
    soup=BeautifulSoup(driver.page_source,'lxml')
    html=soup.select_one('#product-list > div.product-list-view.has-trolley > div.product-list-container > div > div > div.category.product-list--page.product-list--current-page > div > ul')

    department = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(2)')
    category = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(3)')
    sub_category = soup.select_one('#product-list > div.product-list-view.has-trolley > div.breadcrumbs > div > nav > ol > li:nth-child(4)')

    for product in html:
        link = product.find('a', href=True)
        items = {
        'name': product.find('h3', class_='styles__H3-oa5soe-0').text,
        #'price': product.find('p').text,
        #'price per/': product.find('p', class_='styled__StyledFootnote-sc-119w3hf-7').text,
        'product_link': link['href'],
        'department': department.text,
        'category': category.text,
        'sub_category': sub_category.text
        }
        product_list.append(items)



    df = pd.DataFrame(product_list)

    df.to_csv('product.csv')

def main():
    start_time = time.time()



    print('Save whatever')
    with open('links.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            scrape(f"https://www.tesco.com/groceries/en-GB/shop{csv_row['link_url']}")

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f secons.' % time_difference)


main()

 #df = pd.read_csv('links.csv')
    department = 'Chocolates & Biscuits'
    link = 'link_url'
    df2 = df[df['category_name'] == department]
    #print (df2['link_url'])
    link_use = df.loc[df['category_name'] == department]
    web_link = (df2['link_url'].values)
    for aaa in web_link: