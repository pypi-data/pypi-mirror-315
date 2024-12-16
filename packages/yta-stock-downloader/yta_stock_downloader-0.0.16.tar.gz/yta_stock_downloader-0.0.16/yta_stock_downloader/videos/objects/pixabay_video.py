from yta_general_utils.temp import create_temp_filename
from yta_general_utils.downloader import Downloader
from typing import Union


# TODO: Maybe move this to another part (?)
QUALITY_FORMATS_ORDERED = ['large', 'medium', 'small', 'tiny']
"""
This fields are available in the response and
contain all the image formats available for
download.
"""

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
    display_url: str = None
    type: str = None
    """
    TODO: I don't know if this type is useful for us
    """
    duration: float = None
    """
    The video duration provided by the platform.
    """
    views: int = None
    downloads: int = None
    likes: int = None
    author: dict = None

    _best_video: any = None
    _download_url: str = None

    raw_json: dict = None

    def __init__(self, data: any):
        self.id = data['id']
        self.display_url = data['pageURL']
        self.type = data['type']
        self.duration = data['duration']
        self.views = data['views']
        self.downloads = data['downloads']
        self.likes = data['likes']
        self.author = {
            'id': data['user_id'],
            'name': data['user'],
            'avatar_url': data['userImageURL']
        }
        self.raw_json = data

    # TODO: Maybe add 'extension' property to handle
    # it from the end of the 'download_url' property
    
    @property
    def quality(self):
        return self.best_video['quality']
    
    @property
    def thumbnail_url(self):
        return self.best_video['thumbnail']
    
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
    def size(self):
        return self.best_video['size']

    @property
    def best_video(self):
        """
        Best video file for our specific purpose that must
        be loaded on demand to avoid unnecessary processing.
        """
        if self._best_video is None:
            for size in QUALITY_FORMATS_ORDERED:
                if size in self.raw_json['videos']:
                    self._best_video = self.raw_json['videos'][size]
                    break

        return self._best_video
    
    @property
    def download_url(self):
        """
        The url to download the best video file found.
        """
        if self._download_url is None:
            self._download_url = self.best_video['url']

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
            'type': self.type,
            'duration': self.duration,
            'views': self.views,
            'downloads': self.downloads,
            'likes': self.likes,
            'author': self.author,
            'width': self.width,
            'height': self.height,
            'size': self.size,
            'quality': self.quality
        }


"""
"id": 125,
"pageURL": "https://pixabay.com/videos/id-125/",
"type": "film",
"tags": "flowers, yellow, blossom",
"duration": 12,
"videos": {
    "large": {
        "url": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.mp4",
        "width": 1920,
        "height": 1080,
        "size": 6615235,
        "thumbnail": "https://cdn.pixabay.com/video/2015/08/08/125-135736646_large.jpg"
    },
},
"views": 4462,
"downloads": 1464,
"likes": 18,
"comments": 0,
"user_id": 1281706,
"user": "Coverr-Free-Footage",
"userImageURL": "https://cdn.pixabay.com/user/2015/10/16/09-28-45-303_250x250.png"

"""