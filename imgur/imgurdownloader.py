#!/usr/bin/python3


"""
TODO: >add docstring<
"""


import re


class ImgurException(Exception):
    """
    This exception is raised if supplied link is invalid.
    """
    pass


class ImgurDownloader(object):
    """
    ImgurDownloader contains all necessary methods to extract image or
    album images from imgur link.
    """

    def __init__(self, url):
        """
        Initiate ImgurDownloader object.
        """
        self.url = self.sanitize(url)

    def sanitize(self, url):
        """
        Check if the supplied link is valid. If not, raise ImgurException.
        """
        if re.match('https*\:\/\/(i.)*imgur\.com\/', url):
            return url
        raise ImgurException('Invalid link.')

    def is_it_image(self):
        """
        Check if the url points to image. Examples:

        http(s)://i.imgur.com/[image_hash].[extension]
        http(s)://i.imgur.com/[image_hash]
        http(s)://imgur.com/[image_hash]
        """
        pass

    def is_it_album(self):
        """
        Check if the url points to an album. Examples:

        http(s)://imgur.com/a/[album_hash]
        http(s)://imgur.com/gallery/[album_hash]
        """
        pass
