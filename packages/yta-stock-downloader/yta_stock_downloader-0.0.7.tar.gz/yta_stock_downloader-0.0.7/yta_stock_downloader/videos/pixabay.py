from yta_stock_downloader.constants import PIXABAY_VIDEOS_API_ENDPOINT_URL
from yta_general_utils.downloader.video import download_video
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.downloader import Downloader
from typing import Union

import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def search_pixabay_videos(query: str, ignore_ids: list[str] = []):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'pretty': 'true'
    }
    response = requests.get(PIXABAY_VIDEOS_API_ENDPOINT_URL, params = params, timeout = 10)
    #response = requests.get(__get_url(query), timeout = 10)
    response = response.json()

    if response['total'] == 0:
        return []
    
    # TODO: Apply 'ignore_ids'
    
    # TODO: Format videos (?)

def get_first_pixabay_video(query: str, ignore_ids: list[str] = []):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    # TODO: Apply 'ignore_ids'

    videos = search_pixabay_videos(query, ignore_ids)

    if len(videos) == 0:
        raise Exception('No videos found for the provided "query" and "ignore_ids".')
    
    return videos[0]

def download_first_pixabay_video(query: str, ignore_ids: list[str] = [], output_filename: Union[str, None] = None):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    video = get_first_pixabay_video(query, ignore_ids)

    if video is None:
        raise Exception('No video found for the provided "query" and "ignore_ids" list.')

    if not output_filename:
        output_filename = create_temp_filename('tmp_pixabay_video.mp4')

    # TODO: I should handle this about videos in a 
    # specific class to be able to force download
    # directly from the object and that stuff

    # By now I return the first result found
    print(video)
    # videos = response['hits'][0]['videos']

    """
    for video in response['hits']:
        return 
        qualities = video['videos']
        # Qualities come in order, so get the first one by now and thats all
    print(response)

    # response.hits.videos.large,medium,small,tiny
    """


    # TODO: Is it possible to have no size available here (?)
    if url is None:
        raise Exception('WTF?')

    Downloader.download_video(url, output_filename)

    return output_filename

