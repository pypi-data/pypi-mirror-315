from yta_stock_downloader.enums import PexelsLocale
from yta_stock_downloader.constants import PEXELS_SEARCH_VIDEOS_URL, PEXELS_GET_VIDEO_BY_ID_URL
from yta_stock_downloader.videos.objects.pexels_video import PexelsVideo
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader.video import download_video
from yta_general_utils.programming.env import get_current_project_env
from yta_general_utils.programming.parameter_validator import PythonValidator, NumberValidator
# TODO: This is the only 'yta_multimedia' import I have, and it could
# be avoided with the 'rescale_video' function in 'yta_general_utils'.
# Maybe we could simplify this, or maybe we need 'yta_multimedia' 
from yta_multimedia.video.edition.resize import resize_video, ResizeMode
from yta_general_utils.downloader import Downloader
from random import choice
from typing import Union

import requests


PEXELS_API_KEY = get_current_project_env('PEXELS_API_KEY')
RESULTS_PER_PAGE = 25
HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': PEXELS_API_KEY
}

def __search_pexels_videos(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, per_page: int = RESULTS_PER_PAGE):
    response = requests.get(
        url = PEXELS_SEARCH_VIDEOS_URL,
        params = {
            'query': query,
            'locale': locale.value,
            'per_page': per_page
        },
        headers = HEADERS
    )

    # TODO: Should I create a PexelsVideoPageResult (?)
    return [PexelsVideo(video) for video in response.json()['videos']]

    return response.json()['videos']
    page_results = PexelsImagePageResult(query, locale.value, response.json())

    return page_results

def __search_pexels_video(id: int) -> PexelsVideo:
    response = requests.get(
        url = f'{PEXELS_GET_VIDEO_BY_ID_URL}{str(id)}',
        headers = HEADERS
    )
    
    # TODO: Is this actually giving a PexelsVideo (?)
    return PexelsVideo(response.json())

def search_pexels_videos(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids: list[str] = [], per_page: int = 25):
    """
    Obtain videos from Pexels platform according to the 
    provided 'query' and 'locale', including only 
    'per_page' elements per page.
    """
    if not PythonValidator.is_string(query):
        raise Exception('No "query" provided.')
    
    locale = PexelsLocale.to_enum(locale)

    if not NumberValidator.is_positive_number(per_page):
        raise Exception('The provided "duration" parameter is not a positive number.')

    # TODO: Check if this .json()['videos'] is working
    # TODO: Do we need something from the .json() response (?)
    videos = __search_pexels_videos(query, locale, per_page)
    videos = [video for video in videos if video.id not in ignore_ids]

    return videos

def get_first_pexels_video(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids = []) -> PexelsVideo:
    """
    Obtain the first video from the Pexels platform
    according to the provided 'query' and 'locale'
    parameters and avoiding the ones which id is
    contained in the provided 'ignore_ids' parameter
    list.

    This method returns an empty list if no videos
    found with the provided 'query' and 'locale'
    parameters, also according to the provided
    'ignore_ids' ids list.
    """
    videos = search_pexels_videos(query, locale, ignore_ids)

    if len(videos) == 0:
        # TODO: What if no videos available, use next page (?)
        raise Exception('No videos found with the provided "query" and "locale".')
    
    video = videos[0]
    
    return video

def download_first_pexels_video(query: str, locale: PexelsLocale = PexelsLocale.ES_ES, ignore_ids = [], output_filename: Union[str, None] = None):
    video = get_first_pexels_video(query, locale, ignore_ids)

    if not video:
        raise Exception('No video" found for the provided "query" and "locale" parameters.')
    
    if output_filename is None:
        # TODO: Validate 'output_filename'
        output_filename = create_temp_filename('tmp_pexels_video.mp4')

    output_filename = video.download(output_filename)

    return output_filename

def get_pexels_video_by_id(id: int):
    """
    Obtain the pexels video with the provided 'id'
    (if existing).
    """
    if not NumberValidator.is_positive_number(id):
        raise Exception('The provided "id" is not a positive number.')
    
    return __search_pexels_video(id)

def download_pexels_video_by_id(id: int, output_filename: Union[str, None] = None):
    video = get_pexels_video_by_id(id)

    if not video:
        raise Exception('No video found with the given "id".')
    
    if not output_filename:
        # TODO: Validate 'output_filename' if provided
        
        output_filename = create_temp_filename('tmp_pexels_video.mp4')

    output_filename = video.download(output_filename)

    # TODO: What if I cannot download it (?)

    return output_filename







def download_first(query, ignore_ids = [], output_filename = None):
    """
    Searches for the provided 'query', gets the valid results and selects
    the first video that is not included in 'ignore_ids'. If available, it
    downloads that video with the provided 'output_filename' or a temporary
    generated file.

    This method returns an object containing 'id' and 'output_filename' if  
    downloaded, or None if not.
    """
    video = __get_first(query, ignore_ids)

    if not video:
        return None
    
    return __download(video, output_filename)

def download_random(query, ignore_ids = [], output_filename = None):
    """
    Searches for the provided 'query', gets the valid results and selects a
    random video that is not included in 'ignore_ids'. If available, it
    downloads that video with the provided 'output_filename' or a temporary
    generated file.

    This method returns an object containing 'id' and 'output_filename' if  
    downloaded, or None if not.
    """
    video = __get_random(query, ignore_ids)

    if not video:
        return None
    
    return __download(video, output_filename)

def __download(video, output_filename = None):
    """
    Downloads the provided video and returns an object containing 'id'
    and 'output_filename' if downloaded, or None if not.
    """
    if not output_filename:
        output_filename = create_temp_filename('pexels_video.mp4')
    
    output_filename = download_video(video['url'], output_filename)

    return {
        'id': video['id'],
        'output_filename': output_filename
    }

def __get_video_by_id(video_id):
    """
    Obtains the video with the provided 'video_id' from Pexels and
    returns its information as a JSON.
    """
    r = requests.get(f'{PEXELS_GET_VIDEO_BY_ID_URL}{str(video_id)}', headers = HEADERS)

    # TODO: Throw exception if not found
    return r.json()

def __get_first(query, ignore_ids = []):
    """
    Searchss for the provided 'query', gets the valid results and selects 
    the first video that is not included in 'ignore_ids'.

    This method returns a video (containing 'id', 'url', 'width', 'height'
    and 'fps') if found, or None if not.
    """
    videos = __get_videos(query, ignore_ids)

    if len(videos) == 0:
        return None
    
    return videos[0]


def __get_random(query, ignore_ids = []):
    """
    Searchss for the provided 'query', gets the valid results and selects a
    random video that is not included in 'ignore_ids'.

    This method returns a video (containing 'id', 'url', 'width', 'height'
    and 'fps') if found, or None if not.
    """
    videos = __get_videos(query, ignore_ids)

    if len(videos) == 0:
        return None
    
    return choice(videos)

def __get_videos(query, ignore_ids = []):
    """
    This method returns only valid videos found for the provided 'query'. We consider
    valid videos those ones that have a FullHD quality and a aspect ratio close to
    16 / 9, so we can apply some resizing without too much lose. This search will skip
    the videos with any of the 'ignore_ids'.

    This method returns an array of videos (if found) that contains, for each video,
    the main video 'id', 'url', 'width', 'height' and 'fps'. The main video 'id' is
    obtained for avoiding repetitions.
    """
    videos = search_pexels_videos(query)

    best_video_files = []
    if len(videos) > 0:
        for video in videos:
            if video['id'] in ignore_ids:
                continue

            best_video_file = __get_best_video_file(video['video_files'])
            if best_video_file:
                best_video_files.append({
                    'id': video['id'],
                    'url': best_video_file['link'],
                    'width': best_video_file['width'],
                    'height': best_video_file['height'],
                    'fps': best_video_file['fps']
                })

    return best_video_files

def __get_best_video_file(video_files):
    """
    Makes some iterations over received video_files to check the best
    quality video that is hd with the higher 'width' and 'height' values,
    but only accepting (by now) 16/9 format.
    It returns the video if found, or None if there is no valid video available.
    """
    # TODO: This need work
    best_video_file = None
    for video_file in video_files:
        aspect_ratio = video_file['width'] / video_file['height']
        if aspect_ratio < 1.6 or aspect_ratio > 1.95:
            # TODO: We avoid, by now, not valid for resizing
            continue

        # Landscape valid aspect_ratio is 1.7777777777777777 which is 16/9 format
        # Vertical valid aspect ratio is 0.5626 which is 9/16 format
        # TODO: Implement an option to receive vertical format instead of landscape
        if video_file['quality'] != 'sd' and (video_file['width'] > 1920 or video_file['height'] > 1080):
            # This video is valid, lets check if it is the best one
            if best_video_file == None:
                # No previous best_video_file, so this one is the new one
                best_video_file = video_file
            else:
                if best_video_file['width'] < video_file['width']:
                    # More quality, so preserve the new one as best_video
                    best_video_file = video_file

    return best_video_file



def download_video_by_id(pexels_video_id, output_filename = 'download.mp4'):
    """
    Receives a pexels_video_id and downloads to our system that video from
    the Pexels server obtaining the best video quality according to our
    code specifications.
    """
    video_response = __get_video_by_id(pexels_video_id)
    best_video_file = __get_best_video_file(video_response['video_files'])

    # TODO: This should be read from a constants file
    # (that is possibly written in another library)
    SCENE_SIZE = (1920, 1080)

    if best_video_file != None:
        download_video(best_video_file['link'], output_filename)
        if best_video_file['width'] != SCENE_SIZE[0] or best_video_file['height'] != SCENE_SIZE[1]:
            # TODO: Be careful because I'm overwriting the same 
            # video I'm using as output to be written
            # TODO: This has not to be done here as it is part
            # the library who needs it, so we avoid using 
            # 'yta_multimedia'
            resize_video(output_filename, SCENE_SIZE, ResizeMode.RESIZE_KEEPING_ASPECT_RATIO, output_filename)
        return True
    
    return False