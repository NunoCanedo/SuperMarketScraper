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
url='https://www.tesco.com/groceries/en-GB/products/268880284'
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")

    ## Don't need a path, next argument make automation to install if missing
    #webdriver_service = Service("./chromedriver") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
driver.maximize_window()
time.sleep(5)
driver.find_element(By.XPATH,'//*[@id="asparagus-root"]/div/div[2]/main/div/div/div[2]/div/section[2]/div[2]/div[2]/div/div[1]/div/div"]').click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="catch-weight-268880284"]/option[1]').click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[2]').click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[3]').click()
time.sleep(3)
driver.find_element(By.XPATH,'//*[@id="catch-weight-254269241"]/option[4]').click()
time.sleep(5)

#//*[@id="catch-weight-268880284"]
#//*[@id="asparagus-root"]/div/div[2]/main/div/div/div[2]/div/section[2]/div[2]/div[2]/div/div[1]/div/div