import requests 
from bs4 import BeautifulSoup
import csv

import time
import random as rand 

import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()
import json


progress_num = 0
progress_dem = 133

for page in range(0, 20): #Remember to update the number of pages 
    print ("{percent:.2f}% completed".format(percent = progress_num/progress_dem * 100))
    print ("completed {pages} pages".format(pages = page))
    progress_num += 1
    time.sleep(7)
    url = 'https://www.metacritic.com/browse/albums/score/metascore/all/filtered?page=' + str(page)
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = []
    for entity in soup.find_all('a', class_='title'):
        reviews_url = 'https://www.metacritic.com/' + entity['href'] + '/critic-reviews'
        response = session.get(reviews_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try: 
            entity_name = soup.find('div', class_="product_title").find('a').find('h1').text
        except:
            continue
        critics_section = soup.find('div', 'body product_reviews')
        for review_content in critics_section.find_all('div', class_='review_content'):
            score = review_content.find('div', { "class" : ["metascore_w medium album positive indiv perfect", "metascore_w medium album positive indiv", "metascore_w medium album mixed indiv", "metascore_w medium album negative indiv"]}).text
            source = review_content.find('div', class_='source')
            critic_name = ''
            if source.find('a'):
                critic_name = source.find('a').text
            else:
                critic_name = source.text
            review_text = review_content.find('div', class_='review_body')
            date = review_content.find('div', class_='date')
            new_data = {"entity_name" : entity_name, "critic_name" : critic_name, "score" : score, "date" : date.text if date else None}
            reviews.append(new_data)

        try:
            with open("data.json", "w") as final:
                json.dump(reviews, final)
        except IOError:
            print("I/O error")
print (len(reviews))



