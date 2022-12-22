import os
import json

from django.test import TestCase
from django.contrib.auth.models import User

from movie_collection.repositories import movie_collection as movie_collection_repo

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class MovieCollectionTests(TestCase):
    with open(os.path.join(BASE_DIR, 'movies_response.json'), 'r') as json_file:
        GET_MOVIES_RESPONSE = json.load(json_file)

    def create_test_user(self):
        user = User(username="testuser", password="12345")
        user.save()
        self.test_user = user

    def create_movie_collection(self, movies_data):
        self.create_test_user()
        success, movie_collection = movie_collection_repo.create_collection(
            user=self.test_user,
            title='test collection 1',
            description='this is a first test collection',
            movies_data=movies_data,
        )
        if not success:
            raise Exception("Failed to create MovieCollection")
        self.movie_collection = movie_collection

    def test_create_movie_collection(self):
        movies_data = self.GET_MOVIES_RESPONSE.get('results')[:4]
        self.create_movie_collection(movies_data=movies_data)
        self.assertIsNotNone(self.movie_collection)
        self.assertEquals(
            len(movies_data),
            self.movie_collection.movies.count()
        )
        total_unique_genres = set(
            [
                genre_name for movie_data in movies_data[:4]
                for genre_name in movie_data.get("genres").split(",")
                if genre_name
            ]
        )
        self.assertEquals(
            len(total_unique_genres),
            self.movie_collection.movies.filter(
                genres__isnull=False
            ).values_list("genres__name", flat=True).distinct().count()
        )

    def create_multiple_movie_collections(self):
        self.create_test_user()
        self.movie_collections = []
        start_indices = range(0, len(self.GET_MOVIES_RESPONSE['results']), 2)
        stop_indices = range(2, len(self.GET_MOVIES_RESPONSE['results']) + 2, 2)
        for idx, (start, stop) in enumerate(zip(start_indices, stop_indices)):
            movies_data = self.GET_MOVIES_RESPONSE['results'][start:stop]
            success, movie_collection = movie_collection_repo.create_collection(
                user=self.test_user,
                title=f'test collection {idx}',
                description=f'this is a {idx}-th test collection',
                movies_data=movies_data,
            )
            if not success:
                raise Exception("Failed to create MovieCollection")
            self.movie_collections.append(movie_collection)
        return len(start_indices)

    def test_get_user_movie_collection(self):
        collection_source_count = self.create_multiple_movie_collections()
        success, response = movie_collection_repo.get_user_collections(self.test_user)
        self.assertTrue(success)
        self.assertEquals(
            response.get('user_collections').count(),
            collection_source_count
        )
        self.assertLessEqual(
            len(response.get('top_3_genres')),
            3
        )

    def test_update_user_collection(self):
        movies_data = self.GET_MOVIES_RESPONSE.get('results')[:4]
        self.create_movie_collection(movies_data=movies_data)
        success, _ = movie_collection_repo.update_user_collection(
            user=self.test_user,
            uuid=str(self.movie_collection.uuid),
            title=self.movie_collection.title
        )
        self.assertFalse(success)
        success, updated_collection = movie_collection_repo.update_user_collection(
            user=self.test_user,
            uuid=str(self.movie_collection.uuid),
            title=self.movie_collection.title + ' updated'
        )
        self.assertTrue(success)
        self.assertEquals(
            updated_collection.title,
            self.movie_collection.title + ' updated'
        )
        success, updated_collection = movie_collection_repo.update_user_collection(
            user=self.test_user,
            uuid=str(self.movie_collection.uuid),
            description=self.movie_collection.description + ' updated',
        )
        self.assertEquals(
            updated_collection.description,
            self.movie_collection.description + ' updated'
        )
        success, updated_collection = movie_collection_repo.update_user_collection(
            user=self.test_user,
            uuid=str(self.movie_collection.uuid),
            movies_data=self.GET_MOVIES_RESPONSE.get('results')[2:6]
        )
        self.assertEquals(
            len(self.GET_MOVIES_RESPONSE.get('results')[:6]),
            updated_collection.movies.count()
        )

    def test_user_collection_delete(self):
        movies_data = self.GET_MOVIES_RESPONSE.get('results')[:4]
        self.create_movie_collection(movies_data=movies_data)
        success, response = movie_collection_repo.delete_user_collection(
            user=self.test_user, uuid=str(self.movie_collection.uuid)
        )
        self.assertTrue(success)
        self.assertFalse(
            movie_collection_repo.MovieCollection.objects.filter(
                user=self.test_user, uuid=response
            )
        )
