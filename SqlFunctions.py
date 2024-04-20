## IMPORT LIBRARIES

#import requests
import pandas as pd
import mysql.connector
#import PageScraper


#url = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product/taxonomy"


#tree_data = []

## Function to connect Python to MYSQL

def connection_db(database):

    ## Define parametrs to connect python to MYSQL

    db = mysql.connector.connect(
        host = 'localhost',    ## IN MY CASE IS A LOCAL DATABASE
        user = 'YourUserName',    ##INPUT YOUR OWN USERNAME
        passwd = 'YourPasswor',    ## INPUT YOUR OWN PASSWORD
        database = 'SuperMarketScraper'
    )
    
    return db


## Function to connect Python to MYSQL
    
def sql_save_taxonomy(table_name, tree_data):

    ## Define parametrs to connect python to MYSQL

    db = mysql.connector.connect(
        host = 'localhost',    ## IN MY CASE IS A LOCAL DATABASE
        user = 'YourUserName',    ##INPUT YOUR OWN USERNAME
        passwd = 'YourPasswor',    ## INPUT YOUR OWN PASSWORD
        database = 'SuperMarketScraper'
    )
    
    mycursor = db.cursor()

    ## Create table taxonomy

    #table_name = somethi

    query = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (ID int PRIMARY KEY NOT NULL, department VARCHAR(50) NOT NULL, category VARCHAR(50) NOT NULL, aisle VARCHAR(50), shelve VARCHAR(50), web_page_ID int )'

    mycursor.execute(query)
    db.commit()

#def save_data( tree_data):
    ## Loop the values scraped from the webpage and insert in to the table
    for value in tree_data:
        #x = value.get('shleve_ID')

        #query = "INSERT IGNORE INTO " + table_name + " (ID, department, category, aisle, shelve, web_page_ID) VALUES ( %(shleve_ID)s, %(department_name)s, %(category_name)s, %(aisle_name)s, %(shelve)s, %(web_ID)s), value)

        mycursor.execute("INSERT IGNORE INTO " + table_name + " (ID, department, category, aisle, shelve, web_page_ID) VALUES ( %(shleve_ID)s, %(department_name)s, %(category_name)s, %(aisle_name)s, %(shelve)s, %(web_ID)s)", value)
    db.commit()




def SQL_connection(url):

    db = mysql.connector.connect(
        host = 'localhost',    ## IN MY CASE IS A LOCAL DATABASE
        user = 'YourUserName',    ##INPUT YOUR OWN USERNAME
        passwd = 'YourPasswor',    ## INPUT YOUR OWN PASSWORD
        database = 'SuperMarketScraper'
    )

    x = [url]
    table_name = 'Sainsburys_Taxonomy'
    cursor = db.cursor()
    query = 'SELECT ID FROM ' + table_name + ' WHERE web_page_ID = %s' 
    cursor.execute(query, x)
    result = cursor.fetchall()
    code = str(result).replace('[(', '').replace(',)]', '')
    return code





def url(table_name):

    # Open the DataBase to collect the data (web_page_ID)

    db = mysql.connector.connect(
            host = 'localhost',    ## IN MY CASE IS A LOCAL DATABASE
        user = 'YourUserName',    ##INPUT YOUR OWN USERNAME
        passwd = 'YourPasswor',    ## INPUT YOUR OWN PASSWORD
            database = 'SuperMarketScraper'
        )

    table_name = 'Sainsburys_Taxonomy'
    taxonomy = pd.read_sql('SELECT * FROM ' + table_name, db)

# Define only usefull web_page_ID's (WEB PAGE with ALL products are not scraped in this element)
    
    usefull_id = taxonomy.loc[~taxonomy['aisle'].str.contains('All'), ['ID', 'web_page_ID']]
    return usefull_id





## Function to create and insert data into table

def insert_values(page_data, table_name):

    db = mysql.connector.connect(
        host = 'localhost',    ## IN MY CASE IS A LOCAL DATABASE
        user = 'YourUserName',    ##INPUT YOUR OWN USERNAME
        passwd = 'YourPasswor',    ## INPUT YOUR OWN PASSWORD
        database = 'SuperMarketScraper'
    )


    mycursor = db.cursor()

    query = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (Date DATE, ID int, Product VARCHAR(250), Product_Link VARCHAR(250), Price VARCHAR(50), Price_Per VARCHAR(50), Nectar_Price VARCHAR(50), Label VARCHAR(250) )'

    mycursor.execute(query)
    db.commit()

    mycursor = db.cursor()

    for value in page_data:
    
        mycursor.execute("INSERT IGNORE INTO " + table_name + " (Date, ID, Product, Product_Link, Price, Price_Per, Nectar_Price, Label) VALUES ( %(date)s, %(product_ID)s, %(name)s, %(product_link)s, %(price)s, %(price_per)s, %(nectar_price)s,  %(label)s)", value)
        

        db.commit()
