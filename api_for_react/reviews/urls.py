from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path('api/reviews/<int:review_id>/', views.Review.as_view(), name='review'),
    path('api/scrape', views.scrape, name='scrape'),
    path('entitylist', views.entity_list, name='entitylist'),
    path('test', views.slider, name='slider'),
    path('rev', views.review, name='review')
]
