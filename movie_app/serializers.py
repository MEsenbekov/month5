from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director']  # Список полей


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'movie', 'stars']


class MovieWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'director', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            average_rating = sum([review.stars for review in reviews]) / reviews.count()
            return round(average_rating, 2)
        return 0