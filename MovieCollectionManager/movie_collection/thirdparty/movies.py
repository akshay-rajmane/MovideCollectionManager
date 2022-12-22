import os

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

URL = 'https://demo.credy.in/api/v1/maya/movies/'
USERNAME = os.environ.get('MOVIES_SERVICE_USERNAME')
SECRET = os.environ.get('MOVIES_SERVICE_SECRET')
CONNECT_TIMEOUT = 0.2
READ_TIMEOUT = 0.3
MAX_RETRIES = 10



def get_movies(url: str = None):
    """ Fetches paginated movies data """

    url = url or URL
    retries, connect_timeout, read_timeout = 0, CONNECT_TIMEOUT, READ_TIMEOUT
    success, api_response = False, {'message': 'Service unavailable. Please try after sometime.'}
    while retries < MAX_RETRIES:
        try:
            response = requests.get(
                url, auth=(USERNAME, SECRET), timeout=(connect_timeout, read_timeout)
            )
        except (ConnectTimeout, ReadTimeout):
            connect_timeout += connect_timeout
            read_timeout += read_timeout
            retries += 1
        else:
            # If there is an unexpected request error
            if response.status_code != 200:
                retries += 1
                continue
            # If we do not get the movies data
            if (
                (
                    'is_success' in response.json()
                    and response.json().get('is_success') is False
                ) or response.json().get('count') is None
            ):
                retries += 1
                continue
            success, api_response = True, response.json()

    if api_response and 'error' in api_response:
        api_response = {'message': api_response.get('error').get('message')}

    return success, api_response
