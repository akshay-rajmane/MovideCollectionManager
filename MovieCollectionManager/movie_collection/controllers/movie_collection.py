from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from movie_collection.repositories import movie_collection as movie_collection_repo
from movie_collection.helpers.response_helper import JSONResponse
from movie_collection.serializers import movie_collection as movie_collection_serializer


def create_movie_collection(request):
    user = request.user
    request_data = request.data
    if (
        not request_data.get('title')
        or not request_data.get('description')
        or not request_data.get('movies')
    ):
        return JSONResponse(
            data={'message': 'Collection Title, Description and Movies are all required'},
            status=400
        )

    success, response = movie_collection_repo.create_collection(
        user=user,
        title=request_data.get('title'),
        description=request_data.get('description'),
        movies_data=request_data.get('movies'),
    )
    if not success:
        return JSONResponse(
            data={'message': response if response else 'Failed to create collection'},
            status=500
        )

    return JSONResponse(
            data={'collection_uuid': str(response.uuid)},
            status=200
        )


def get_user_movie_collections(request):
    success, response = movie_collection_repo.get_user_collections(
        user=request.user
    )
    if not success:
        return JSONResponse(
            data={'is_success': success, 'message': response if response else 'Failed to fetch collections'},
            status=500
        )

    response_data = {
        'is_success': success,
        'data': {
            'collections': (
                movie_collection_serializer.MovieCollectionSerializerBasic(
                    response.get('user_collections'), many=True
                ).data if response.get('user_collections') else None
            ),
            'favourite_genres': response.get('top_3_genres')
        }
    }
    return JSONResponse(data=response_data, status=200)


def get_user_movie_collection_by_uuid(request, uuid: str):
    if not uuid:
        return JSONResponse(
            data={'message': 'Collection UUID is required'},
            status=400
        )

    success, response = movie_collection_repo.get_user_collection(
        user=request.user, uuid=uuid
    )
    if not success:
        return JSONResponse(
            data={'message': response if response else 'Failed to fetch collection'},
            status=500
        )

    return JSONResponse(
        data=movie_collection_serializer.MovieCollectionSerializerDetailed(response).data,
        status=200
    )


def update_user_movie_collection(request, uuid):
    if not uuid:
        return JSONResponse(
            data={'message': 'Collection UUID is required'},
            status=400
        )

    if (
        not request.data.get('title')
        and not request.data.get('description')
        and not request.data.get('movies')
    ):
        return JSONResponse(
            data={'message': 'At least one of Title, Description or Movies is required'},
            status=400
        )
    success, response = movie_collection_repo.update_user_collection(
        user=request.user,
        uuid=uuid,
        title=request.data.get('title'),
        description=request.data.get('description'),
        movies_data=request.data.get('movies'),
    )
    if not success:
        return JSONResponse(
            data={'message': response if response else 'Failed to update collection'},
            status=500
        )

    return JSONResponse(
        data=movie_collection_serializer.MovieCollectionSerializerDetailed(response).data,
        status=200
    )


def delete_user_movie_collection(request, uuid):
    if not uuid:
        return JSONResponse(
            data={'message': 'Collection UUID is required'},
            status=400
        )

    success, response = movie_collection_repo.delete_user_collection(
        user=request.user, uuid=uuid
    )
    if not success:
        return JSONResponse(
            data={'message': response if response else 'Failed to delete collection'},
            status=500
        )

    return JSONResponse(
        data={'deleted_collection_uuid': response},
        status=200
    )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def movie_collection(request, **kwargs):
    if request.method == 'GET':
        if kwargs.get('uuid'):
            return get_user_movie_collection_by_uuid(request, uuid=kwargs.get('uuid'))
        return get_user_movie_collections(request)
    if request.method == 'POST':
        return create_movie_collection(request)
    if request.method == 'PUT':
        return update_user_movie_collection(request, uuid=kwargs.get('uuid'))
    if request.method == 'DELETE':
        return delete_user_movie_collection(request, uuid=kwargs.get('uuid'))
    
