from movie_collection.models import Genre


def get_or_create(genre_name):
    genre, _ = Genre.objects.get_or_create(name=genre_name)
    genre.save()
    return True, genre
