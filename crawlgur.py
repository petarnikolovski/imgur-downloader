#!/usr/bin/python3


"""
TODO: Add >how to<
"""


from argparse import ArgumentParser


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

    print(verbose, url, destination)
