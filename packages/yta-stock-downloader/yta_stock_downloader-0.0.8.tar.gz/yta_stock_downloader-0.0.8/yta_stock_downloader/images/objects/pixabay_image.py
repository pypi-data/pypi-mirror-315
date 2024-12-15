


# TODO: Maybe move this to another part (?)
QUALITY_FORMATS_ORDERED = ['imageURL', 'fullHDURL', 'largeImageURL', 'webformatURL', 'previewURL']
"""
This fields are available in the response and
contain all the image formats available for
download.
"""

class PixabayImage:
    id: str = None
    """
    Unique identifier of this image in Pixabay
    platform. Useful to avoid using it again
    in the same project.
    """
    width: int = None
    height: int = None
    size: int = None
    """
    Size (in bytes?) of the image.
    """
    display_url: str = None
    """
    Url in which the image is displayed in the
    Pixabay platform. This url is not for 
    downloading the image.
    """
    _download_url: str = None
    """
    The download url of the option with the highest
    quality available. This download url is found in
    the 'src' attribute by searching in desc. order.
    """
    tags: str = None
    """
    Tags used when uploading the image to Pixabay
    platform.
    """
    author: dict = None
    """
    Author information.
    """
    raw_json: dict = None
    """
    The whole raw json data provided by Pexels. This
    is for debugging purposes only.
    """

    @property
    def download_url(self):
        """
        The download url of the option with the highest
        quality available. This download url is found in
        different attributes of the whole response, by
        searching in desc. order.
        """
        if self._download_url is None:
            for field in QUALITY_FORMATS_ORDERED:
                # TODO: The field is actually in the response, not nested
                if self[field]:
                    self._download_url = self[field]

        return self._download_url

    def __init__(self, data: any):
        self.id = data['id']
        self.width = data['imageWidth']
        self.height = data['imageHeight']
        self.size = data['imageSize']
        self.display_url = data['pageURL']
        self.tags = data['tags']
        self.author = {
            'id': data['user_id'],
            'name': data['user'],
            'avatar_url': data['userImageURL']
        }
        self.raw_json = data



    """
    "id": 195893,
        "pageURL": "https://pixabay.com/en/blossom-bloom-flower-195893/",
        "type": "photo",
        "tags": "blossom, bloom, flower",
        "previewURL": "https://cdn.pixabay.com/photo/2013/10/15/09/12/flower-195893_150.jpg"
        "previewWidth": 150,
        "previewHeight": 84,
        "webformatURL": "https://pixabay.com/get/35bbf209e13e39d2_640.jpg",
        "webformatWidth": 640,
        "webformatHeight": 360,
        "largeImageURL": "https://pixabay.com/get/ed6a99fd0a76647_1280.jpg",
        "fullHDURL": "https://pixabay.com/get/ed6a9369fd0a76647_1920.jpg",
        "imageURL": "https://pixabay.com/get/ed6a9364a9fd0a76647.jpg",
        "imageWidth": 4000,
        "imageHeight": 2250,
        "imageSize": 4731420,
        "views": 7671,
        "downloads": 6439,
        "likes": 5,
        "comments": 2,
        "user_id": 48777,
        "user": "Josch13",
        "userImageURL": "https://cdn.pixabay.com/user/2013/11/05/02-10-23-764_250x250.jpg",
    """