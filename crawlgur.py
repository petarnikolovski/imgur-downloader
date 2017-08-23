#!/usr/bin/python3


"""
Imgur Downloader downloads single images or albums from imgur.com. These are types
of links that are allowed as input:

~ http(s)://i.imgur.com/[image_hash].[extension]
~ http(s)://i.imgur.com/[image_hash]
~ http(s)://imgur.com/[image_hash]
~ http(s)://imgur.com/a/[album_hash]
~ http(s)://imgur.com/gallery/[album_hash]

How to use app? Here is an example:

python3 crawlgur.py -v https://imgur.com/a/album_id /path/to/directory
"""


from argparse import ArgumentParser
from imgur.imgur import Imgur
from imgur.downloader import Downloader


__author__ = 'petarGitNik'
__copyright__ = 'Copyright (c) 2017 petarGitNik petargitnik@gmail.com'
__license__ = 'MIT'
__version__ = 'v0.2.0'
__email__ = 'petargitnik@gmail.com'
__status__ = 'Production'


def parse_arguments():
    """
    Parse input arguments of the program.
    """
    parser = ArgumentParser(description='Imgur downloader')

    parser.add_argument('-v', '--verbose',
                        help='display download progress and information',
                        action='store_true')
    parser.add_argument('URL', help='source link')
    parser.add_argument('directory', help='destination directory')

    args = parser.parse_args()

    return (args.verbose, args.URL, args.directory)


if __name__ == '__main__':
    verbose, url, destination = parse_arguments()

    imgur = Imgur(url)
    imgur.prepare_images()
    imgur.numerate_images()

    downloader = Downloader(imgur.images, destination, verbose)
    downloader.download()
