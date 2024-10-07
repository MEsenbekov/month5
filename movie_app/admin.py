from django.contrib import admin
from movie_app.models import Movie, Director, Review

admin.site.register(Movie)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'text', 'stars')
    search_fields = ('text',)
    list_filter = ('stars',)
    fields = ('movie', 'text', 'stars')

# Register your models here.
