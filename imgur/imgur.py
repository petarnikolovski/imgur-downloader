#!/usr/bin/python3


"""
This module contains classes for parsing the imgur.com site. It consists of three
classes:

~ ImgurException
~ ImgurFileFormats
~ Imgur

Imgur is the main class and it obtains list of direct image urls that could be
used to download images. Example usage:

```python3
imgur = Imgur('http://imgur.com/gallery/vTTHZ')
imgur.prepare_images()
images = imgur.images
```

imgur.images is a deque of two keyed dictionaries. Example usage:

```python3
for image in images:
    print(image['url'], image['filename'])
```

If images need to be downloaded in order they appear in an album, their filenames
have to be numerated. Full examples:

```python3
imgur = Imgur('http://imgur.com/gallery/vTTHZ')
imgur.prepare_images()
imgur.images # These are not guaranteed to appear in order when downloaded

imgur.numerate_images()
images = imgur.images
```
"""


import re
from collections import deque
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__license__ = 'MIT'
__version__ = 'v0.2.0'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Production'


class ImgurException(Exception):
    """
    This exception is raised if supplied link is invalid.
    """
    pass


class ImgurFileFormats(object):
    """
    Contains extensions for file formats that are allowed on imgur. Source:

    https://help.imgur.com/hc/en-us/articles/115000083326-What-files-can-I-upload-

    Archived:
    http://archive.is/89Uky
    https://web.archive.org/web/20170222111303/https://help.imgur.com/hc/en-us/articles/115000083326-What-files-can-I-upload-
    """
    JPG = '.jpg'
    JPEG = '.jpeg'
    PNG = '.png'
    GIF = '.gif'
    APNG = '.apng'
    TIFF = '.tiff'
    PDF = '.pdf'
    XCF = '.xcf'
    #WEBM = '.webm'
    #MP4 = '.mp4'

    @classmethod
    def formats(cls):
        """
        Return a set consisting of all class attributes. Class attributes must
        not be callable.
        """
        formats = set()
        for attribute in ImgurFileFormats.__dict__.keys():
            if attribute[:2] != '__':
                value = getattr(ImgurFileFormats, attribute)
                if not callable(value):
                    formats.add(value)
        return formats


class Imgur(object):
    """
    Imgur contains all necessary methods to extract image or album images from
    imgur link.
    """

    def __init__(self, url):
        """
        Initiate Imgur object.
        """
        self.url = self.sanitize(url)
        self.images = deque()

    def sanitize(self, url):
        """
        Check if the supplied link is valid. If not, raise ImgurException. This
        method checks only if the domain is valid.
        """
        if re.match('https?\:\/\/(i\.|www\.)?imgur\.com\/', url):
            if self.is_it_gifv(url):
                return self.sanitize_gifv(url)
            return url
        raise ImgurException('Invalid link.')

    def sanitize_gifv(self, url):
        """
        Remove 'v' from .gifv
        """
        pattern = 'https?\:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.gif'
        return re.match(pattern, url).group(0)

    def is_it_gifv(self, url):
        """
        Check if the supplied link points to .gifv page.
        """
        if '.gifv' in url:
            return True
        return False

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

    def turn_into_grid(self):
        """
        Append ?grid to url.
        """
        if self.is_it_album():
            if not self.is_it_grid():
                return ''.join([self.change_gallery(), '?grid'])
            else:
                return self.url
        raise ImgurException('Cannot convert single image into album grid.')

    def prepare_images(self):
        """
        Parses HTML from the provided url to obtain link(s) to image(s). Raises
        exception if the link already ends with an extension.
        """
        if self.is_it_image():
            if self.contains_extension(self.url):
                self.images.append(
                        self.pack_image(self.url, self.get_image_filename(self.url))
                    )
                return
            else:
                self.parse_and_prepare_images(self.url)
                return
        grid = self.turn_into_grid()
        self.parse_and_prepare_images(grid)
        return

    def parse_and_prepare_images(self, url):
        """
        Obtain and parse html, and append image dictionaries to image deque.
        """
        pattern = '\{"hash":"([a-zA-Z0-9]+)".*?"ext":"([\.a-zA-Z0-9\?\#]+)".*?\}'
        try:
            html = urlopen(url).read().decode('utf-8')
            filenames_with_duplicates = re.findall(pattern, html)
            filenames_clean = self.remove_duplicates(filenames_with_duplicates)
            urls = self.build_image_url_list(filenames_clean)
            for url in urls:
                self.images.append(
                    self.pack_image(url, self.get_image_filename(url))
                )
        except HTTPError as e:
            print(e.status)
        except URLError as e:
            print(e.reason)

    def build_image_url_list(self, filenames):
        """
        Build list of direct links to images. Input filenames list is a list of
        tuples e.g. [('jedEzFL', '.jpg'), ('lciC5G8', '.jpg')]. The output looks
        like:
        ['https://i.imgur.com/jedEzFL.jpg', 'https://i.imgur.com/lciC5G8.jpg']
        """
        urls = []
        for filename, extension in filenames:
            urls.append(''.join(['https://i.imgur.com/', filename, extension]))
        return urls

    def remove_duplicates(self, filenames):
        """
        Remove duplicates from a list of tuples containing filenames with
        extensions.
        """
        clean = []
        for filename in filenames:
            if filename not in clean:
                clean.append(filename)
        return clean

    def contains_extension(self, url):
        """
        Check if the image url contains extension. If there is an extension it
        is returned. Otherwise, None is returned.
        """
        for extension in ImgurFileFormats.formats():
            if extension in url:
                return extension
        return None

    def get_image_filename(self, url):
        """
        Get image file name from its url. Examples:

        https://i.imgur.com/jedEzFL.jpg     ->  jedEzFL.jpg
        https://i.imgur.com/jedEzFL.jpg?1   ->  jedEzFL.jpg
        """
        candidate = url.split('/')[-1]
        extension = self.contains_extension(url)
        pattern = ''.join(['.+\\', extension])
        return re.match(pattern, candidate).group(0)

    def pack_image(self, url, filename):
        """
        Returns a dictionary with image url and corresponding filename.
        """
        return {'url' : url, 'filename' : filename}

    def number_of_images(self):
        """
        Get the number of images from the images attribute.
        """
        return len(self.images)

    def numerate_images(self):
        """
        Append ordinal number to image filename.
        """
        total = self.digits_in_a_number(len(self.images))
        ordinal = '{0:0%dd}' % total
        for index, image in enumerate(self.images, start=1):
            image['filename'] = ''.join([
                    ordinal.format(index), '-', image['filename']
                ])

    def digits_in_a_number(self, number):
        """
        Return how many digits are there in a number.
        """
        return len(str(number))
