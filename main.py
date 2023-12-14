##Tesco data search(taxanomy/tree)
#To get all links on the web page


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



url = 'https://www.tesco.com/groceries/en-GB/taxonomy'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
data = requests.get(url,headers=headers).json()



##Loop the taxanomy tree to get the final links for each sub-category

#Maybe usefull to have a lists to organize ID for eacho product in not so rawdom order
department_list = []
category_list = []
sub_category_list = []



#should look how to make a exclusion list for seasonal links to save time and resources  because produts will be displayed on other section

#exclusion_list = []

def something():
    start_time = time.time()


    
    print('Save whatever')
    with open('links.csv') as file:
        csv_reader = csv.DictReader(file)
        for csv_row in csv_reader:
            for csv_row in csv_reader:
                scrape(f"https://www.tesco.com/groceries/en-GB/shop{csv_row['link_url']}")
    

    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f secons.' % time_difference)



link_list = []


# Function to find all URL from the website taxonomy tree

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





    # Save links in a csv file

    df = pd.DataFrame(link_list)

    df.to_csv('links.csv')
    time_difference = time.time() - start_time
    print(f'Scraping time: %.2f secons.' % time_difference)

    something()




    

if __name__ == '__main__':
    link_url()





    




    
