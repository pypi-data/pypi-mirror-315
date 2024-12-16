from yta_stock_downloader.constants import PIXABAY_API_ENDPOINT_URL
from yta_stock_downloader.images.objects.pixabay_image import PixabayImage
from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.temp import create_temp_filename
from typing import Union

import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def __search_pixabay_images(query: str):
    return requests.get(
        PIXABAY_API_ENDPOINT_URL,
        {
            'key': PIXABAY_API_KEY,
            'q': query,
            'image_type': 'photo'
        },
        timeout = 10
    )

def search_pixabay_images(query: str, ignore_ids: list[str] = []) -> list[PixabayImage]:
    """
    Search the images with the provided 'query' in
    the Pixabay platform.

    This method returns an empty array if no images
    found, or the array containing the images if
    found.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    response = __search_pixabay_images(query).json()

    if response['total'] == 0:
        return []
    
    images = [PixabayImage(image) for image in response['hits']]
    images = [image for image in images if image.id not in ignore_ids]
    
    return images

def get_first_pixabay_image(query: str, ignore_ids: list[str]) -> PixabayImage:
    """
    Find and return the first image from Pixabay provider
    with the given 'query' (if existing).

    The result will be None if no results, or a result
    containing the first one found.

    TODO: Maybe create a object to map response (?)
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    images = search_pixabay_images(query, ignore_ids)

    if len(images) == 0:
        return None
    
    return images[0]

def download_first_pixabay_image(query: str, ignore_ids: list[str], output_filename: Union[str, None] = None):
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

    image_to_download = get_first_pixabay_image(query, ignore_ids)

    if image_to_download is None:
        raise Exception(f'No available images for the provided query "{query}".')
    
    if not output_filename:
        output_filename = create_temp_filename('tmp_pexels_image.png')

    output_filename = image_to_download.download(output_filename)

    # if not downloaded:
    #     raise Exception(f'Something went wrong when trying to download the found Pexels image from the url "{download_url}".')

    return output_filename