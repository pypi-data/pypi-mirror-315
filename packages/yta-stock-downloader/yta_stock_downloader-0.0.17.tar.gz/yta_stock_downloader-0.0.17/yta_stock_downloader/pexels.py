from yta_stock_downloader.images.pexels import get_first_pexels_image, download_first_pexels_image
from yta_stock_downloader.videos.pexels import get_first_pexels_video, download_first_pexels_video
from yta_stock_downloader.enums import PexelsLocale
from typing import Union


class Pexels:
    """
    Class to provide images and videos from the Pexels
    platform.

    This class uses the Pexels API and our registered
    API key to obtain the results.

    See: https://www.pexels.com/
    """
    @staticmethod
    def get_first_image(query: str, locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES, ignore_ids: list[int] = []):
        """
        Obtain the first available image from the Pexels
        provider for the given 'query' and 'locale' (if
        available).

        This method raises an Exception if no image 
        available.
        """
        return get_first_pexels_image(query, locale, ignore_ids)
    
    @staticmethod
    def download_first_image(query: str, locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES, ignore_ids: list[int] = [], output_filename: Union[str, None] = None):
        """
        Download the first available image from the Pexels
        provider for the given 'query' and 'locale' (if
        available).

        This method raises an Exception if no image 
        available or if the download is not possible.
        """
        return download_first_pexels_image(query, locale, ignore_ids, output_filename)

    @staticmethod
    def get_first_video(query: str, locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES, ignore_ids: list[int] = []):
        """
        Obtain the first available video from the Pexels
        provider for the given 'query' and 'locale' (if
        available).
        
        This method raises an Exception if no video
        available or if the download is not possible.
        """
        return get_first_pexels_video(query, locale, ignore_ids)

    @staticmethod
    def download_first_video(query: str, locale: Union[PexelsLocale, str] = PexelsLocale.ES_ES, ignore_ids: list[int] = [], output_filename: Union[str, None] = None):
        """
        Download the first available video from the Pexels
        provided and the given 'query' and locale' (if
        existing) avoiding the ones in the 'ignore_ids' 
        list.

        This method raises an Exception if no video
        available to download or if the download is
        not possible.
        """
        return download_first_pexels_video(query, locale, ignore_ids, output_filename)