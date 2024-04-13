## Import Libraries

from bs4 import BeautifulSoup
import time




## Function to join MULTIPLE INTEGERS into a single INTEGER (NUMBER)

def numConcat(num1, num2, num3, num4):
  return int("{}{}{}{}".format(num1, num2, num3, num4))





## Function to TRY and Extract the individual data from each product in the Page being scraped
        
def extract_data(product, selector):
  try:
    return product.select_one(selector).text
  except AttributeError:
    return None
  

## Function to join the page ID with the product ID to generate a unique product ID
  
def product_code(num1, num2):
  return int("{}{}".format(num1, num2))



