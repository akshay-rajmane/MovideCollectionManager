import uuid

from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True, editable=False)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    uuid = models.CharField(max_length=200, primary_key=True, db_index=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.title


class MovieCollection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_collections')
    title = models.CharField(max_length=200)
    description = models.TextField()
    movies = models.ManyToManyField(Movie)

    def __str__(self) -> str:
        return self.title
