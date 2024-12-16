from yta_general_utils.downloader import Downloader
from yta_general_utils.temp import create_temp_filename
from typing import Union


# TODO: Maybe move this to another part (?)
FIELDS_ON_SRC = ['original', 'large2x', 'large', 'medium', 'small', 'portrait', 'landscape', 'tiny']
"""
This fields are available in the 'src' attribute
which contains all the image formats available
for download.
"""

class PexelsImage:
    """
    Class to represent a Pexels image and to
    simplify the way we work with its data.
    """
    id: int = None
    """
    Unique identifier of this image in Pexels
    platform. Useful to avoid using it again
    in the same project.
    """
    width: int = None
    height: int = None
    display_url: str = None
    """
    Url in which the image is displayed in the
    Pexels platform. This url is not for 
    downloading the image.
    """
    _download_url: str = None
    """
    The download url of the option with the highest
    quality available. This download url is found in
    the 'src' attribute by searching in desc. order.
    """
    src: dict = None
    """
    The different image formats (within a dict)
    available for download. See FIELDS_ON_SRC to
    see available formats.
    """
    author: dict = None
    """
    The author of the image as a dict containing
    its name, profile url and id.
    """
    agerage_color: str = None
    """
    The average color of the image, provided by
    the Pexels platform.
    """
    is_liked: bool = None
    """
    A boolean that indicates if I have liked the
    image or not.
    """    
    alt: str = None
    """
    The alternative text of the image, which is a
    useful description for web browsers.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def download_url(self):
        """
        The download url of the option highest quality
        option available. This download url is found in
        the 'src' attribute by searching in desc. order.
        """
        if self._download_url is None:
            for field in FIELDS_ON_SRC:
                if self.src[field]:
                    self._download_url = self.src[field]
                    break

        return self._download_url

    def __init__(self, data):
        # TODO: Could be some of those fields unavailable?
        self.id = data['id']
        self.width = data['width']
        self.height = data['height']
        self.display_url = data['url']
        self.src = data['src']
        self.author = {
            'id': data['photographer_id'],
            'url': data['photographer_url'],
            'name': data['photographer'],
        }
        self.average_color = data['avg_color']
        """
        These are the different formats available: 'original', 
        'large2x', 'large', 'medium', 'small', 'portrait',
        'landscape' and 'tiny'
        """
        self.is_liked = data['liked']
        self.alt = data['alt']
        self.raw_json = data

    def download(self, output_filename: Union[str, None] = None):
        """
        Download this image to the provided local
        'output_filename'. If no 'output_filename'
        is provided, it will be stored locally with
        a temporary name.

        This method returns the final downloaded
        image filename.
        """
        if output_filename is None:
            output_filename = create_temp_filename('tmp_pexels_image.png')

        Downloader.download_image(self.download_url, output_filename)

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
            'display_url': self.display_url,
            'download_url': self.download_url,
            'author': self.author,
            'average_color': self.average_color,
            'src': self.src,
            'is_liked': self.is_liked, 
            'alt': self.alt,
        }

        # TODO: I do it manually to fit the same structure
        return self.__json