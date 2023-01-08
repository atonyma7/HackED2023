from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import time
from bs4 import BeautifulSoup
from math import sqrt
from numpy import std
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review as ReviewModel, Entity as EntityModel, Userscore as UserscoreModel
from .serializers import *
from requests_html import HTMLSession
from django.http import HttpResponse
from django.db.models import Avg
from django.template import loader
from rest_framework.views import APIView
from .forms import ReviewForm

class Review(APIView):
    #get review by id to display on review page
    def get_review(self, review_id):
        return get_object_or_404(ReviewModel, id=review_id)

    #get request to display review
    def get(self, request, review_id):
        review = self.get_review(review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


def scrape(request):
    progress_num = 0
    progress_dem = 20
    session = HTMLSession()
    for page in range(0, 10): #Remember to update the number of pages 
        print ("{percent:.2f}% completed".format(percent = progress_num/progress_dem * 100))    #progress bar
        print ("completed {pages} pages".format(pages = page))  
        progress_num += 1
        time.sleep(5)
        url = 'https://www.metacritic.com/browse/albums/score/metascore/all/filtered?page=' + str(page) 
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser') #parse the html
        reviews = []
        #get all the reviews
        for block in soup.find_all('tr', class_=None):  
            img_src = block.find('img')['src']  #get the image source
            metascore = block.find(
                'div', { "class" : [
                    "metascore_w large release positive", 
                    "metascore_w large release mixed", 
                    "metascore_w large release negative"]}
                    ).text    #get the metascore
            entity = block.find('a', class_='title')    #get the entity name
            reviews_url = 'https://www.metacritic.com/' + entity['href'] + '/critic-reviews'
            response = session.get(reviews_url) 
            soup = BeautifulSoup(response.text, 'html.parser')  
            #try to get the entity name, if it fails, skip
            try: 
                entity_name = soup.find('div', class_="product_title").find('a').find('h1').text
            except:
                continue
            #create the entity if it doesn't exist
            newEntity = EntityModel.objects.create(name=entity_name, metascore=metascore, img_src=img_src)
            critics_section = soup.find('div', 'body product_reviews')
            for review_content in critics_section.find_all('div', class_='review_content'):
                score = review_content.find(
                    'div', { "class" : [
                        "metascore_w medium album positive indiv perfect", 
                        "metascore_w medium album positive indiv", 
                        "metascore_w medium album mixed indiv", 
                        "metascore_w medium album negative indiv"]}
                        ).text   #get the score
                source = review_content.find('div', class_='source')     
                critic_name = ''
                if source.find('a'):
                    critic_name = source.find('a').text
                else:
                    critic_name = source.text
                review_text = review_content.find('div', class_='review_body')
                date = review_content.find('div', class_='date')
                try:
                    ReviewModel.objects.create(
                        entity_name=entity_name, date=date, score=score, 
                        publication=critic_name, entity=newEntity)
                except:
                    continue
    html = "<html><body>Finished</body></html>"
    return HttpResponse(html)

def entity_list(request):
    dev_list = []
    #get the standard deviation of each entity
    for entity in EntityModel.objects.all():
        #get the scores of each review for the entity
        entity_scores = ReviewModel.objects.filter(entity=entity).values_list('score', flat=True).order_by('id')
        std_dev = std(list(entity_scores))
        #add the entity to the list
        dev_list.append({
            "entity_name" : entity.name, "std_dev" : std_dev, 
            "metascore" : entity.metascore, "img_src" : entity.img_src})
        
    return render(request, 'entity_list.html', {"list": dev_list})
# Create your views here.

def slider(request):

    template = loader.get_template('slider.html')
    return HttpResponse(template.render())
def entity(request, entity_id):
    entity = get_object_or_404(EntityModel, id=entity_id)
    if request.method == 'POST':
        UserscoreModel.objects.update_or_create(entity=entity, defaults = {"userscore" : request.POST['user_score']})

    entity_scores = ReviewModel.objects.filter(entity=entity).values_list('score', flat=True).order_by('id')
    std_dev = std(list(entity_scores))
    userscore = UserscoreModel.objects.filter(entity=entity)[0].userscore
    entity_dict = {"entity_name" : entity.name, "std_dev" : std_dev, "metascore" : entity.metascore, "img_src" : entity.img_src, "userscore" : userscore}
    form = ReviewForm()

    return render(request, 'entity.html', {"dict" : entity_dict, "form" : form})
def similar(request):
    critic_dict = {}
    for userscore in UserscoreModel.objects.all():
        print (ReviewModel.objects.filter(entity=userscore.entity))
        for review in ReviewModel.objects.filter(entity=userscore.entity):
            if review.publication in critic_dict.keys():
                critic_dict[review.publication] += (userscore.userscore - review.score)
            else:
                critic_dict[review.publication] = (userscore.userscore - review.score)
    sorted_dict = dict(sorted(critic_dict.items(), key=lambda x: abs(x[1])))
    print (sorted_dict)
    return render(request, 'similar.html', {"data" : sorted_dict})