from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path('api/reviews/<int:review_id>/', views.Review.as_view(), name='review'),
]