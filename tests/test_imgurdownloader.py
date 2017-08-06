#!/usr/bin/python3


import pytest
from imgur.imgurdownloader import ImgurDownloader
from imgur.imgurdownloader import ImgurException


class TestImgurDownloader(object):
    """
    Class that tests imgur downloader class from the main package.
    """

    def test_invalid_link(self):
        """
        Test if the class raises exception for invalid link.
        """
        with pytest.raises(ImgurException):
            ImgurDownloader('https://www.reddit.com')

    def test_invalid_link_with_variation(self):
        """
        Test if the class raises exception for invalid link.
        """
        with pytest.raises(ImgurException):
            ImgurDownloader('https://www.reddit.com/imgur.com')
