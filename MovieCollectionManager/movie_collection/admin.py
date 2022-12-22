from django.contrib import admin

from movie_collection import models

class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)

admin.site.register(models.Genre, GenreAdmin)


class MovieAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('uuid', 'title',)

admin.site.register(models.Movie, MovieAdmin)


class MovieCollectionAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('uuid', 'title',)

admin.site.register(models.MovieCollection, MovieCollectionAdmin)
