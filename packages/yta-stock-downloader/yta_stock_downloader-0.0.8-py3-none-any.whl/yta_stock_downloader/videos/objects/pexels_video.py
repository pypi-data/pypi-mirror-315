


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
    url: str = None
    width: int = None
    height: int = None
    fps: float = None
    video_files: list = None
    _best_video_file: any = None

    def __init__(self, id: str, url: str, width: int, height: int, fps: float, video_files: list):
        # TODO: Raise Exception if invalid video initialization (?)
        self.id = id
        self.url = url
        self.width = width
        self.height = height
        self.fps = fps
        self.video_files = video_files

    @property
    def best_video_file(self):
        """
        Best video file for our specific purpose that must
        be loaded on demand to avoid unnecessary processing.
        """
        if self.best_video_file is None:
            best_one = None
            # TODO: Apply strategy to look for the best one
            for video_file in self.video_files:
                # TODO: This was the previous strategy but we must
                # update and improve it because it seems to be very
                # sh*tty
                aspect_ratio = video_file['width'] / video_file['height']
                if aspect_ratio < 1.6 or aspect_ratio > 1.95:
                    # TODO: We avoid, by now, not valid for resizing
                    continue

                # Landscape valid aspect_ratio is 1.7777777777777777 which is 16/9 format
                # Vertical valid aspect ratio is 0.5626 which is 9/16 format
                # TODO: Implement an option to receive vertical format instead of landscape
                if video_file['quality'] != 'sd' and (video_file['width'] > 1920 or video_file['height'] > 1080):
                    # This video is valid, lets check if it is the best one
                    if best_one == None:
                        # No previous best_video_file, so this one is the new one
                        best_one = video_file
                    else:
                        if best_one['width'] < video_file['width']:
                            # More quality, so preserve the new one as best_video
                            best_one = video_file

                self._best_video_file = best_one

        return self._best_video_file