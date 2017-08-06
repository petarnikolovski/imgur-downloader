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
        if re.match('https*\:\/\/[i.]*imgur\.com', url):
            return url
        raise ImgurException('Invalid link.')
