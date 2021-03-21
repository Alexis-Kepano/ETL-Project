from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import os
import pandas as pd
import requests
from pprint import pprint
import time
import pymongo

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.driver.maximize_window()

# URL of page to be scraped
url_base = "http://quotes.toscrape.com/"
next_page_link=''

quote_everything=[] #collection of everything associated with the quotes
quote_list=[] #collection of quotes
author_info=[] #collection of author information
tag_relation=[] #collection for tag and quote relation
unique_tags=[] #stores unique tags
tags=[]#used to store a collection of tags

while True:
    url=url_base+next_page_link
    browser.visit(url)
    html=browser.html
    quote_soup=BeautifulSoup(html,'html.parser')
    quotes=quote_soup.find_all('div',class_='quote')
    #loops each quote on the web page quotes.toscrape.com
    

    for quote in quotes:
        #finds the quote text
        q_text = quote.find('span',class_="text").text
        #print(q_text)
        #finds all tags 
        q_tags = quote.find_all('a',class_="tag")

        #list to store all tags
        tag_list=[]
        #loops through the quote tags and adds it to tag list
        for tag in q_tags:
            for t in tag:
                if t not in unique_tags:
                    unique_tags.append(t)
                    tags.append({"tag":t})
                    
            tag_text=tag.text
            tag_list.append(tag_text)
        
        #visiting author page
        #get author link
        try:
            #get link to author's page
            author_link = quote.find('a')['href']
            #print(author_link)
            #got to author's page
            browser.visit(url_base+author_link)
#           time.sleep(10)
            html2=browser.html
            #get the html soup from author_link
            author_soup=BeautifulSoup(html2,'html.parser')
            #get author_details from author_soup
            author_details=author_soup.find('div',class_='author-details')
            #get author's name from author_details
            author_name = author_details.find('h3').text
            #get author's birth date and place from author_details 
            author_born=author_details.find('span',class_='author-born-date').text + " "+ author_details.find('span',class_='author-born-location').text
            #get the description of the author
            author_description=author_details.find('div',class_="author-description").text
            #creates a dictionary for quote, tag, author's name, born, and description 
            quote_everything_dict={"quote_text":q_text,"tags":tag_list,"author_name":author_name,"author_born":author_born,"author_description":author_description}
            quote_dict={"quote_text":q_text,"author_name":author_name}
            author_info_dict={"name":author_name,"born":author_born,"description":author_description}
           
            tags_dict={"quote_text":q_text,"tag":tag_list}
            #stores dictionaries in a quote_list, author_info, tag_relation
            quote_list.append(quote_dict)
            author_info.append(author_info_dict)
            quote_everything.append(quote_everything_dict)
            tag_relation.append(tags_dict)
            browser.back()
        except Exception as e:
            print("Scraping Author Page Complete")
            break
            
        
            
    try:
        next_page = quote_soup.find('li',class_='next')
        next_page_link = next_page.find('a')['href']
        #browser.close()
        #print(next_page_link)
    except Exception as e:
        print(f"Scraping Quotes Page Complete")
        break
        
browser.quit()  
pprint(len(quote_list))

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
#creates a data base quotes_db
db=client.quotes_db
#creates a collections for database quotes_db
db.quotes.drop()
db.quotes_everything_collection.drop()
db.quotes_collection.drop()
db.author_information_collection.drop()
db.tag_relation_collection.drop()
db.tags_collection.drop()
#-------------------------------------------------------
#insert collections as a MongoDB document
collection_1 = db.quotes_everything_collection
collection_2=db.quotes_collection
collection_3=db.author_information_collection
collection_4=db.tag_relation_collection
collection_5 = db.tags_collection
collection_1.insert_many(quote_everything)
collection_2.insert_many(quote_list)
collection_3.insert_many(author_info)
collection_4.insert_many(tag_relation)
collection_5.insert_many(tags)