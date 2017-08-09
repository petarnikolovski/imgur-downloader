#!/usr/bin/python3


"""
Download images from imgur. Use this in combination with Imgur class.
Example:

```python3
from imgur.imgurdownloader Import Imgur

imgur = Imgur('http(s)://imgur.com/[album_hash]')
imgur.prepare_images()
imgur.numerate_images()
```
"""

import os
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import URLError
from shutil import copyfileobj
from time import sleep

class Downloader(object):
    """
    This class downloads files from provided source.
    """

    def __init__(self, images, destination, verbose=False):
        self.images = images
        self.destination = destination
        self.verbose = verbose
        self.current_directory = os.getcwd()
