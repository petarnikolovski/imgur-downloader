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
        Check if the supplied link is valid. If not, raise ImgurException. This
        method checks only if the domain is valid.
        """
        if re.match('https*\:\/\/(i\.)?imgur\.com\/', url):
            return url
        raise ImgurException('Invalid link.')

    def is_it_image(self):
        """
        Check if the url points to image. Examples:

        http(s)://i.imgur.com/[image_hash].[extension]
        http(s)://i.imgur.com/[image_hash]
        http(s)://imgur.com/[image_hash]
        """
        # https*\:\/\/(i\.)?imgur\.com\/[a-zA-Z0-9]*(\.[a-zA-Z]{1,4})?
        return not self.is_it_album()

    def is_it_album(self):
        """
        Check if the url points to an album. Examples:

        http(s)://imgur.com/a/[album_hash]
        http(s)://imgur.com/gallery/[album_hash]
        """
        return ('/a/' in self.url) or ('/gallery/' in self.url)

    def is_it_grid(self):
        """
        Check if the url points to a grid view. Example:

        http(s)://imgur.com/a/[album_hash]?grid
        """
        return self.url.endswith('?grid')

    def change_gallery(self):
        """
        Change /gallery/ to /a/ in url.
        """
        return self.url.replace('/gallery/', '/a/')
