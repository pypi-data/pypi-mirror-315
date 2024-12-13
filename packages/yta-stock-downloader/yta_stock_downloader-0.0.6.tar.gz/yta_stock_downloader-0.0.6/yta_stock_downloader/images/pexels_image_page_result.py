from yta_stock_downloader.images.pexels_image import PexelsImage
from yta_stock_downloader.enums import PexelsLocale


class PexelsImagePageResult:
    """
    A class to represent the results obtaining by the
    Pexels Image API requests we fire, including all 
    the information needed to be able to work with the
    obtained images and look for more.
    """
    query: str = None
    """
    The query used in the request.
    """
    locale: PexelsLocale = None
    """
    The locale used in the request.
    """
    page: int = None
    """
    The current page of Pexels image results.
    """
    per_page: int = None
    """
    The amount of images that are being obtained
    per page for the request.
    """
    total_results: int = None
    """
    The amount of results obtained with the request,
    that is the sum of all existing results 
    considering not pagination nor current page.

    TODO: Is this actually that value (?)
    """
    next_page_api_url: str = None
    """
    The API url to make a request to obtain the next
    results page.
    """
    images: list[PexelsImage] = None
    """
    The array containing all the images found in the
    current page according to the query.
    """

    @property
    def total_pages(self):
        total = (int) (self.total_results / self.per_page)
        if self.total_results % self.per_page > 0:
            total += 1

        return total

    def __init__(self, query, locale, data):
        self.query = query
        self.locale = locale
        self.page = data['page']
        self.per_page = data['per_page']
        self.total_results = data['total_results']
        # We calculate the total pages
        self.total_pages = (int) (self.total_results / self.per_page)
        if self.total_results % self.per_page > 0:
            self.total_pages += 1
        self.next_page_api_url = data['next_page'],
        self.photos = []

        for photo in data['photos']:
            self.photos.append(PexelsImage(photo))

    def json(self):
        return {
            'query': self.query,
            'locale': self.locale,
            'page': self.page,
            'per_page': self.per_page,
            'total_results': self.total_results,
            'total_pages': self.total_pages,
            'next_page_api_url': self.next_page_api_url,
            'photos': self.photos
        }

        # TODO: This below is not working
        from json import dumps as json_dumps

        return json_dumps(self.__dict__) 