from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Review as ReviewModel
from .serializers import *
from django.shortcuts import render, get_object_or_404


from rest_framework.views import APIView


class Review(APIView):
    def get_review(self, review_id):
        return get_object_or_404(ReviewModel, id=review_id)

    def get(self, request, review_id):
        review = self.get_review(review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

# Create your views here.
