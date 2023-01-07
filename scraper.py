import requests 
from bs4 import BeautifulSoup

import time
import random as rand 

import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

review_dict = {'id':[], 'score':[], 'publication':[], 'entity_name':[]}

for page in range(0,134): #Remember to update the number of pages 
    url = 'https://www.metacritic.com/browse/albums/score/metascore/all/filtered?page=' + str(page)
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for entity in soup.find_all('a', class_='title'):
        print (entity)
