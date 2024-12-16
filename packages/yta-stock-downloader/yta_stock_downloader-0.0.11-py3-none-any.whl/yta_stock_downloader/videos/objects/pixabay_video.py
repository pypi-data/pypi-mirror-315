from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader import Downloader
from typing import Union


class PixabayVideo:
    """
    Class to represent a video of the Pixabay platform and
    to handle it easier than as raw data. A video has the
    main information but also different video formats and
    qualities that can be used for different purposes.
    Maybe we want a landscape video or maybe a portrait, so
    both of them could be available as 'video_files' for
    the same video content.
    """
    id: str = None
    """
    Unique identifier for this video in the Pixabay
    platform.
    """
    sizes: list = None
    all_formats: list = None
    _best_video: any = None
    _download_url: str = None

    def __init__(self, id: str, data: any):
        # TODO: Raise Exception if invalid video initialization (?)
        self.id = id
        self.all_formats = [] # TODO: Load this
        self.data = data

    @property
    def quality(self):
        return self.best_video['quality']
    
    @property
    def file_type(self):
        """
        The MIME type of the video expressed in the
        'video/mp4' format.
        """
        return self.best_video['file_type']
    
    @property
    def width(self):
        """
        The width in pixels of the best option of
        this video.
        """
        return self.best_video['width']
    
    @property
    def height(self):
        """
        The height in pixels of the best option of
        this video.
        """
        return self.best_video['height']
    
    @property
    def fps(self):
        return self.best_video['fps']
    
    @property
    def size(self):
        return self.best_video['size']

    @property
    def best_video(self):
        """
        Best video file for our specific purpose that must
        be loaded on demand to avoid unnecessary processing.
        """
        if self._best_video is None:
            for size in ['large', 'medium', 'small', 'tiny']:
                if size in self.all_formats:
                    self._best_video = self.all_formats[size]
                    break

        return self._best_video
    
    @property
    def download_url(self):
        """
        The url to download the best video file found.
        """
        if self._download_url is None:
            self.download_url = self.best_video['url']

        return self._download_url
    
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
            output_filename = create_temp_filename('tmp_pixabay_video.mp4')

        output_filename = Downloader.download_video(self.download_url)

        return output_filename
    
    def as_json(self):
        """
        Return the object instance as a json to be
        displayed and debugged.
        """
        return {
            'id': self.id,
            'width': self.width,
            'height': self.height,
            'size': self.size,
            'fps': self.fps,
            'file_type': self.file_type,
            'quality': self.quality
        }


    """
    "videos": {
        "large": {
            "url": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.mp4",
            "width": 1920,
            "height": 1080,
            "size": 6615235,
            "thumbnail": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.jpg"
    """

    """
    ['large', 'medium', 'small', 'tiny']:
        if size in videos:
            url = videos[size]['url']
    """
    