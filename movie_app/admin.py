from django.contrib import admin
from movie_app.models import *

admin.site.register(Movie)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Здесь указываешь, какие поля будут отображаться в списке
    search_fields = ('name',)  # Поля, по которым можно будет производить поиск

# Register your models here.
