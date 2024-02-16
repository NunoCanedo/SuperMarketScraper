#Import Libraries

import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from csv import DictReader



products_list = []
products_to_scrape = []


## Starter URL
url = 'https://www.tesco.com/groceries/en-GB/taxonomy'
## Define headers or will not get a reponse
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
data = requests.get(url,headers=headers).json()

#Parametres to scrape the Page
#Needs to be worked out o be able to scrape without open a browser
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")

## Don't need a path, next argument make automation to install if missing
#webdriver_service = Service("./chromedriver") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

##This are the main and the usefull departments in the website, all the other links as seasonal 
usefull_links = ['Fresh Food', 'Bakery', 'Frozen Food', 'Treats & Snacks', 'Food Cupboard', 'Drinks', 'Baby & Toddler', 'Health & Beauty', 'Pets', 'Household', 'Home & Ents']

##May create a exception list too, TO BE LOOKED LATER <------
exceptions_links = []



## Function to avoid errors when different data or unvalable data is displayed in the WebPage

def extract_data(product, selector):
    try:
        return product.select_one(selector).text
    except AttributeError:
        return None



## Function to loop and scrape data from each product

def Product_data(soup):

    

    html=soup.select_one('#product-list > div.product-list-view.has-trolley > div.product-list-container > div > div > div.category.product-list--page.product-list--current-page > div > ul')
#<span class="styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text">Tesco Sirloin Steak 227G</span>
#<h3 class="styles__H3-oa5soe-0 gbIAbl"><a href="/groceries/en-GB/products/300400609" class="styled__Anchor-sc-1i711qa-0 hXcydL ddsweb-link__anchor" data-auto="product-tile--title" data-di-id="di-id-f1d56516-270f138d"><span class="styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text">Tesco Sirloin Steak 227G</span></a></h3>
    ## Loop the list of products in the page to get necessary data
    for product in html:
        items = {
        'name': extract_data(product, 'h3.styles__H3-oa5soe-0'),
        'price': extract_data(product, 'p.styled__StyledHeading-sc-119w3hf-2'),
        #This is for product were weight have to be selected
        'price_weight': extract_data(product, 'div.base-components__RootElement-sc-1mosoyj-1.styled__Container-sc-16t2b2a-0.jptQqM.PUfgZ.styled__StyledFormGroup-sc-6nhkzi-2.hidpNF.beans-buybox__weight-input-controls.beans-buybox__form-group.beans-form-group__container > div'), ## May need de product number for specific cases
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
            print(products_list)
            print('========================')

        else:
            products_to_scrape.append(items)
            print(products_to_scrape)
    
    
    #if products_list.get('price_weight') == None:
    #print(products_list)

    #for item in products_list:
        #print(item)
    #//*[@id="groceries"]/div/div[2]/ul/li[1]/ul/li[2]/ul/li[2]/a
            #//*[@id="groceries"]/div/div[2]/ul/li[1]/ul/li[2]/ul/li[1]/a
            

products = pd.DataFrame(products_list)
list_to_scrape = pd.DataFrame(products_to_scrape) 

products.to_csv('products_csv')
list_to_scrape.to_csv('list_to_scrape_csv')
       

    

    


#def parser_url(url):

    #Parametres to scrape the Page
    #Needs to be worked out o be able to scrape without open a browser 

    


## Function to loop through all the URL's who get colected before
def page_to_scrape(csv_file, name):
    link_page = open(csv_file, 'r')
    web_page = DictReader(link_page)

    for page in web_page:
        if page.get('department_name') == name:
            url_link = page.get('link_url')
            url = f"https://www.tesco.com/groceries/en-GB/shop{url_link}"
            
            
            driver.get(url)
            driver.maximize_window()
            time.sleep(5)

            ## Next parameters aren't needed but may be usefull
            #accept cookie
            #driver.find_element(By.XPATH,'//*[@id="onetrust-button-group-parent"]/div/button[1]').click()
            #time.sleep(2)
            soup=BeautifulSoup(driver.page_source,'lxml')
            
            Product_data(soup)
                    
            

        else:
            pass




## Function to define only usefull departments
def department_to_scrape(list):
    
    for name in usefull_links:
        department = name

        page_to_scrape('new_links_csv', name)




##Loop the taxanomy tree to get the final links for each sub-category

#Maybe usefull to have a lists to organize ID for eacho product in not so rawdom order
department_list = []
category_list = []
sub_category_list = []


##should look how to make a exclusion list for seasonal links to save time and resources  because produts will be displayed on other section

#exclusion_list = []



link_list = []


## Function to find all URL from the website taxonomy tree

def link_url():
    start_time = time.time()
    for department in data:
        for category in department.get('children'):

            # Exception were CHILDREN is a empty list
            
            if category.get('children') == None:
                pass

            else:
                for sub_category in category.get('children'):

                    # Exception were URL is a empty list

                    if sub_category.get('url') == None:
                        pass

                    else:

                        #Exception to avoid all SUB_CATEGORIES as one single link

                        if sub_category.get('label') == 'department':
                            pass

                        else:
                            sub_category_list.append(sub_category.get('url'))

                            #Create a dict to save the extrated data(links)

                            link = {
                                'department_name': department.get('name'),
                                'category_name': category.get('name'),
                                'sub_category_name': sub_category.get('name'),
                                'link_url': sub_category.get('url')
                            }

                            # append the list created to main list

                            link_list.append(link)
                            

    headers_list = ['department_name', 'category_name', 'sub_category_name', 'link_url']



    ## Save links in a csv file

    with open('new_links_csv', 'w', newline='') as new_links_csv:
        writer = csv.DictWriter(new_links_csv, fieldnames=headers_list)

        writer.writeheader()
        writer.writerows(link_list)



    department_to_scrape(usefull_links)




    

if __name__ == '__main__':
    link_url()





    




    
