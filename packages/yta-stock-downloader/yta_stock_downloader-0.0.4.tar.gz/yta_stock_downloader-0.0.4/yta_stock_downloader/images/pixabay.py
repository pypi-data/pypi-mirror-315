from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.url import encode_url_parameters
from typing import Union

import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def __get_url(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo'
    }

    return f'https://pixabay.com/api/?{encode_url_parameters(params)}'

def get_first_pixabay_image(query: str):
    """
    Find and return the first image from Pixabay provider
    with the given 'query' (if existing).

    The result will be None if no results, or a result
    containing, at least, an 'largeImageUrl' attribute.

    TODO: Maybe create a object to map response (?)
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    response = requests.get(__get_url(query), timeout = 10)
    response = response.json()

    if response['total'] == 0:
        return None
    
    return response['hits'][0]

def download_first_pixabay_image(query: str, output_filename: Union[str, None] = None):
    """
    Download the first found pexels image with the provided
    "query". The image will be stored locally as
    'output_filename' or as a temporary filename if that
    parameter is not provided. The stored image filename is
    returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    image_to_download = get_first_pixabay_image(query)

    if image_to_download is None:
        raise Exception(f'No available images for the provided query "{query}".')
    
    if not output_filename:
        output_filename = create_temp_filename('tmp_pexels_image.png')

    download_url = image_to_download['largeImageURL']
    downloaded = download_image(download_url, output_filename)

    if not downloaded:
        raise Exception(f'Something went wrong when trying to download the found Pexels image from the url "{download_url}".')

    return output_filename