from yta_stock_downloader.images.pexels_image import PexelsImage
from yta_stock_downloader.constants import PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL
from yta_stock_downloader.images.pexels_image_page_result import PexelsImagePageResult
from yta_stock_downloader.enums import PexelsLocale
from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_general_utils.temp import create_temp_filename
from typing import Union

import requests


PEXELS_API_KEY = get_current_project_env('PEXELS_API_KEY')

HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': PEXELS_API_KEY
}


def search_pexels_images(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids: list[str] = [], per_page: int = 25, page: int = 1) -> PexelsImagePageResult:
    """
    Makes a search of Pexels images and returns the results.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    locale = PexelsLocale.to_enum(locale)

    if not NumberValidator.is_positive_number(per_page):
        raise Exception('The provided "duration" parameter is not a positive number.')
    
    if not NumberValidator.is_positive_number(page):
        raise Exception('The provided "page" parameter is not a positive number.')

    params = {
        'query': query,
        'orientation': 'landscape',   # landscape | portrait | square
        'size': 'large',   # large | medium | small
        'locale': locale.value, # 'es-ES' | 'en-EN' ...
        'per_page': per_page,
        'page': page
    }
    response = requests.get(PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL, params = params, headers = HEADERS)
    page_results = PexelsImagePageResult(query, locale.value, response.json())

    # TODO: Apply 'ignore_ids'

    return page_results

def get_first_pexels_image(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids: list[str] = []) -> PexelsImage:
    """
    Find and return the first image from Pexels provider
    with the given 'query' and 'locale' parameters (if
    existing).

    The result will be None if no results, or an object that 
    contains the 'id', 'width', 'height', 'url'. Please, see
    the PexelsImage class to know about the return.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    locale = PexelsLocale.to_enum(locale)
    
    results = search_pexels_images(query, locale, ignore_ids, 1)

    # TODO: Maybe throw Exception instead of None (?)
    if not results:
        return None
    
    return results[0]

def download_first_pexels_image(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids: list[str] = [], output_filename: Union[str, None] = None) -> str:
    """
    Download the first found pexels image with the provided
    "query" and the also given "locale". The image will be
    stored locally as 'output_filename' or as a temporary
    filename if that parameter is not provided. The stored
    image filename is returned.

    This method will raise an Exception if no images are
    found or if the download is not possible.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')

    locale = PexelsLocale.to_enum(locale)

    image_to_download = get_first_pexels_image(query, locale, ignore_ids)

    if image_to_download is None:
        raise Exception(f'No available images for the provided query "{query}" with locale "{locale.value}".')

    if not output_filename:
        output_filename = create_temp_filename('tmp_pexels_image.png')

    download_url = image_to_download.src['landscape']
    downloaded = download_image(download_url, output_filename)

    if not downloaded:
        raise Exception(f'Something went wrong when trying to download the found Pexels image from the url "{download_url}".')

    return output_filename