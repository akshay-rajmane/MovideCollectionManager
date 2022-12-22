from django.contrib.auth.models import User
from django.db.models import Count

from movie_collection.models import MovieCollection
from movie_collection.repositories import movie as movie_repo


def create_collection(user: User, title: str, description: str, movies_data: list):
    """Creates a new MovieCollection for a user"""

    if MovieCollection.objects.filter(title=title).exists():
        return False, "Another collection with the same title already exists. Please use different title"

    movie_collection = MovieCollection.objects.create(
        user=user,
        title=title,
        description=description,
    )
    for movie_data in movies_data:
        success, movie = movie_repo.get_or_create(**movie_data)
        if success:
            movie_collection.movies.add(movie)
    movie_collection.save()
    return True, movie_collection


def get_user_collection(user: User, uuid: str):
    """Fetches User's single MovieCollection based on UUID"""

    user_collections = MovieCollection.objects.filter(user=user, uuid=uuid).first()
    return True, user_collections


def get_user_collections(user: User):
    """Fetches a User's MovieCollections with top 3 Genres"""

    result = {"user_collections": None, "top_3_genres": None}
    user_collections = MovieCollection.objects.filter(user=user)
    if not user_collections:
        return True, result
    top_3_genres = user_collections.filter(movies__genres__isnull=False).annotate(
        genre_count=Count("movies__genres__name")
    ).values_list("movies__genres__name", flat=True).order_by("-genre_count")[:3]
    result["user_collections"] = user_collections
    result["top_3_genres"] = list(top_3_genres) if top_3_genres else None
    return True, result


def update_user_collection(
    user: User, uuid: str, title: str = None, description: str = None, movies_data: list = None
):
    user_collection = MovieCollection.objects.filter(user=user, uuid=uuid).first()
    if not user_collection:
        return False, "Collection not found"

    if title:
        if MovieCollection.objects.filter(title=title).exists():
            return False, "Another collection with the same title already exists. Please use different title"
        user_collection.title = title

    if description:
        user_collection.description = description

    if movies_data:
        if not isinstance(movies_data, list):
            return False, "New movies data is invalid"
        for movie_data in movies_data:
            success, movie = movie_repo.get_or_create(**movie_data)
            if success:
                user_collection.movies.add(movie)

    user_collection.save()
    return True, user_collection


def delete_user_collection(user: User, uuid: str):
    user_collection = MovieCollection.objects.filter(user=user, uuid=uuid).first()
    if not user_collection:
        return False, "Collection not found"
    collection_uuid = str(user_collection.uuid)
    user_collection.delete()
    return True, collection_uuid
