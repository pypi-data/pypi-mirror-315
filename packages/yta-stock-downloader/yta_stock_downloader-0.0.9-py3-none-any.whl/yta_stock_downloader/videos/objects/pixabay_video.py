


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
    sizes: list = None
    all_formats: list = None
    _best_video_quality: any = None

    def __init__(self, id: str, data: any):
        # TODO: Raise Exception if invalid video initialization (?)
        self.id = id
        self.all_formats = [] # TODO: Load this
        self.data = data

    @property
    def _best_video_quality(self):
        """
        Best video file for our specific purpose that must
        be loaded on demand to avoid unnecessary processing.
        """
        if self._best_video_quality is None:
            for size in ['large', 'medium', 'small', 'tiny']:
                if size in self.all_formats:
                    self._best_video_quality = self.all_formats[size]
                    break

        return self._best_video_quality

    """
    ['large', 'medium', 'small', 'tiny']:
        if size in videos:
            url = videos[size]['url']
    """
    