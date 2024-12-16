from yta_stock_downloader.constants import PIXABAY_VIDEOS_API_ENDPOINT_URL
from yta_stock_downloader.videos.objects.pixabay_video import PixabayVideo
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.downloader import Downloader
from typing import Union

import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def __search_pixabay_videos(query: str):
    response = requests.get(
        url = PIXABAY_VIDEOS_API_ENDPOINT_URL,
        params = {
            'key': PIXABAY_API_KEY,
            'q': query,
            'pretty': 'true'
        },
        timeout = 10
    )

    return response.json()

def search_pixabay_videos(query: str, ignore_ids: list[str] = []):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    response = __search_pixabay_videos(query)

    if response['total'] == 0:
        return []
    
    videos = [PixabayVideo(video) for video in response['hits']]
    videos = [video for video in videos if video.id not in ignore_ids]

    return videos

def get_first_pixabay_video(query: str, ignore_ids: list[str] = []):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    videos = search_pixabay_videos(query, ignore_ids)

    if len(videos) == 0:
        return None
    
    return videos[0]

def download_first_pixabay_video(query: str, ignore_ids: list[str] = [], output_filename: Union[str, None] = None):
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    video = get_first_pixabay_video(query, ignore_ids)

    if video is None:
        raise Exception('No video found for the provided "query" and "ignore_ids" list.')

    if not output_filename:
        output_filename = create_temp_filename('tmp_pixabay_video.mp4')

    output_filename = video.download(output_filename)

    return output_filename


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

