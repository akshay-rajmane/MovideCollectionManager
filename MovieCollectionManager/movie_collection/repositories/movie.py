from movie_collection.models import Movie
from movie_collection.repositories import genre as genre_repo


def get_or_create(uuid: str, title: str, description: str, genres: str):
    """Creates new Movie with related Genre"""

    movie = Movie.objects.filter(uuid=uuid).first()
    if movie:
        return True, movie

    movie = Movie.objects.create(
        uuid=uuid,
        title=title,
        description=description,
    )
    if genres:
        genre_names = [genre_name for genre_name in genres.split(',') if genre_name]
        for genre_name in genre_names:
            success, genre = genre_repo.get_or_create(genre_name=genre_name)
            if success:
                movie.genres.add(genre)
    movie.save()
    return True, movie
