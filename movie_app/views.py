from django.db.models import Avg
from django.shortcuts import render

from . import models
from .models import Director, Movie, Review
from rest_framework import generics

from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer


class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class MovieReviewListAPIView(generics.ListAPIView):
    serializer_class = MovieWithReviewsSerializer

    def get_queryset(self):
        return Movie.objects.prefetch_related('reviews').annotate(average_rating=Avg('reviews__stars'))

# Create your views here.
