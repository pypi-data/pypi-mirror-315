from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader import Downloader
from typing import Union


class PexelsVideo:
    """
    Class to represent a video of the Pexels platform and
    to handle it easier than as raw data. A video has the
    main information but also different video files, or
    video formats, that can be used for different purposes.
    Maybe we want a landscape video or maybe a portrait,
    so both of them could be available as 'video_files'
    for the same video content.
    """
    id: str = None
    """
    The video unique identifier in the Pexels platform.
    """
    display_url: str = None
    width: int = None
    height: int = None
    duration: float = None
    thumbnail_url: str = None
    author: dict = None
    """
    The author of the image as a dict containing
    its name, profile url and id.
    """
    video_files: list[any] = None
    """
    A list containing all the video source files for
    this specific video.
    """
    _best_video: dict = None
    """
    The video source with the best quality which is
    actually stored on the platform.

    TODO: Rethink this because it is a complex dict
    with 'file_type' and more properties we should
    map to be handled easier
    """
    _download_url: str = None
    """
    The url to download the best video file found.
    """
    fps: float = None
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def best_video(self):
        """
        The video source with the best quality which is
        actually stored on the platform.
        """
        if self._best_video is None:
            # TODO: What if lower quality but higher fps value (?)
            self._best_video = max(self.video_files, key = lambda video_file: video_file['width'])

        return self._best_video
    
    @property
    def download_url(self):
        """
        The url to download the best video file found.
        """
        if self._download_url is None:
            self._download_url = self.best_video['link']

        return self._download_url
    
    @property
    def fps(self):
        return self.best_video['fps']

    def __init__(self, data: any):
        self.id = data['id']
        self.display_url = data['url']
        self.width = data['width']
        self.height = data['height']
        self.duration = data['duration']
        self.thumbnail_url = data['image']
        self.author = {
            'id': data['user']['id'],
            'url': data['user']['url'],
            'name': data['user']['name'],
        }
        # TODO: Add author
        self.video_files = data['video_files']
        self.raw_json = data

    def download(self, output_filename: Union[str, None] = None):
        """
        Download this video to the provided local
        'output_filename'. If no 'output_filename'
        is provided, it will be stored locally with
        a temporary name.

        This method returns the final downloaded
        video filename.
        """
        if not output_filename:
            output_filename = create_temp_filename('tmp_pexels_video.mp4')

        output_filename = Downloader.download_video(self.download_url, output_filename)

        return output_filename
    
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        return {
            'id': self.id,
            'display_url': self.display_url,
            'width': self.width,
            'height': self.height,
            'duration': self.duration,
            'thumbnail_url': self.thumbnail_url,
            'author': self.author,
            'download_url': self.download_url,
        }


    # @property
    # def best_video_file(self):
    #     """
    #     Best video file for our specific purpose that must
    #     be loaded on demand to avoid unnecessary processing.
    #     """
    #     if self.best_video_file is None:
    #         best_one = None
    #         # TODO: Apply strategy to look for the best one
    #         for video_file in self.video_files:
    #             # TODO: This was the previous strategy but we must
    #             # update and improve it because it seems to be very
    #             # sh*tty
    #             aspect_ratio = video_file['width'] / video_file['height']
    #             if aspect_ratio < 1.6 or aspect_ratio > 1.95:
    #                 # TODO: We avoid, by now, not valid for resizing
    #                 continue

    #             # Landscape valid aspect_ratio is 1.7777777777777777 which is 16/9 format
    #             # Vertical valid aspect ratio is 0.5626 which is 9/16 format
    #             # TODO: Implement an option to receive vertical format instead of landscape
    #             if video_file['quality'] != 'sd' and (video_file['width'] > 1920 or video_file['height'] > 1080):
    #                 # This video is valid, lets check if it is the best one
    #                 if best_one == None:
    #                     # No previous best_video_file, so this one is the new one
    #                     best_one = video_file
    #                 else:
    #                     if best_one['width'] < video_file['width']:
    #                         # More quality, so preserve the new one as best_video
    #                         best_one = video_file

    #             self._best_video_file = best_one

    #     return self._best_video_file