from yta_stock_downloader.images.pixabay import get_first_pixabay_image, download_first_pixabay_image
from yta_stock_downloader.videos.pixabay import get_first_pixabay_video, download_first_pixabay_video
from typing import Union


class Pixabay:
    """
    Class to provide images and videos from the Pixabay
    platform.

    This class uses the Pixabay API and our registered
    API key to obtain the results.

    See: https://pixabay.com/
    """
    def get_first_image(query: str, ignore_ids: list[int] = []):
        """
        Obtain the first available image from the Pexels
        provider for the given 'query' (if available).

        This method raises an Exception if no image 
        available.
        """
        return get_first_pixabay_image(query, ignore_ids)
    
    @staticmethod
    def download_first_image(query: str, ignore_ids: list[int] = [], output_filename: Union[str, None] = None):
        """
        Download the first available image from the Pexels
        provider for the given 'query' (if available).

        This method raises an Exception if no image 
        available or if the download is not possible.
        """
        return download_first_pixabay_image(query, ignore_ids, output_filename)
    
    @staticmethod
    def get_first_video(query: str, ignore_ids: list[int] = []):
        """
        Obtain the first available video from the Pixabay
        provider for the given 'query' and 'locale' (if
        available).
        
        This method raises an Exception if no video
        available or if the download is not possible.

        TODO: Review the explanation
        """
        return get_first_pixabay_video(query, ignore_ids)
    
    @staticmethod
    def download_first_video(query: str, ignore_ids: list[int] = [], output_filename: Union[str, None] = None):
        """
        Download the first available video from the Pixabay
        provided and the given 'query' (if existing)
        avoiding the ones in the 'ignore_ids' list.

        This method raises an Exception if no video
        available to download or if the download is
        not possible.
        """
        return download_first_pixabay_video(query, ignore_ids, output_filename)
