from rest_framework.serializers import ModelSerializer, SerializerMethodField

from movie_collection.models import MovieCollection, Movie


class MovieSerializer(ModelSerializer):
    genres = SerializerMethodField()
    def get_genres(self, movie):
        return list(movie.genres.values_list("name", flat=True).distinct())

    class Meta:
        model = Movie
        fields = (
            "uuid",
            "title",
            "description",
            "genres",
        )


class MovieCollectionSerializerBasic(ModelSerializer):
    class Meta:
        model = MovieCollection
        fields = (
            "uuid",
            "title",
            "description",
        )


class MovieCollectionSerializerDetailed(ModelSerializer):
    movies = SerializerMethodField()
    def get_movies(self, movie_collection):
        return MovieSerializer(movie_collection.movies.all(), many=True).data
    class Meta:
        model = MovieCollection
        fields = (
            "title",
            "description",
            "movies",
        )
