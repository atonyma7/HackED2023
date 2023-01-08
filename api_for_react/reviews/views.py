from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import time
from bs4 import BeautifulSoup


from .models import Review as ReviewModel
from .serializers import *
from django.shortcuts import render, get_object_or_404
from requests_html import HTMLSession

from rest_framework.views import APIView


class Review(APIView):
    def get_review(self, review_id):
        return get_object_or_404(ReviewModel, id=review_id)

    def get(self, request, review_id):
        review = self.get_review(review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

def scrape(request):
    progress_num = 0
    progress_dem = 20
    session = HTMLSession()
    for page in range(0, 20): #Remember to update the number of pages 
        print ("{percent:.2f}% completed".format(percent = progress_num/progress_dem * 100))
        print ("completed {pages} pages".format(pages = page))
        progress_num += 1
        time.sleep(5)
        url = 'https://www.metacritic.com/browse/albums/score/metascore/all/filtered?page=' + str(page)
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        for block in soup.find_all('tr', class_=None):
            img_src = block.find('img')['src']
            entity = block.find('a', class_='title')
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
                try:
                    ReviewModel.objects.create(name=entity_name, date=date, score=score, publication=critic_name, img_src=img_src)
                except:
                    continue
    html = "<html><body>Finished</body></html>"
    return HttpResponse(html)

# Create your views here.
