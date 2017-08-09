#!/usr/bin/python3


import pytest
from collections import deque
from imgur.imgurdownloader import Imgur
from imgur.imgurdownloader import ImgurException


@pytest.fixture
def single_image_i():
    return Imgur('http://i.imgur.com/jedEzFL.jpg')

@pytest.fixture
def single_image_without_extension_i():
    return Imgur('http://i.imgur.com/jedEzFL')

@pytest.fixture
def single_image_without_extension():
    return Imgur('http://imgur.com/jedEzFL')

@pytest.fixture
def album_a():
    return Imgur('http://imgur.com/a/vTTHZ')

@pytest.fixture
def album_grid():
    return Imgur('http://imgur.com/a/vTTHZ?grid')

@pytest.fixture
def album_gallery():
    return Imgur('http://imgur.com/gallery/vTTHZ')

def test_invalid_link():
    """
    Test if the class raises exception for invalid link.
    """
    with pytest.raises(ImgurException):
        Imgur('https://www.reddit.com')

def test_invalid_link_with_variation():
    """
    Test if the class raises exception for invalid link.
    """
    with pytest.raises(ImgurException):
        Imgur('https://www.reddit.com/imgur.com')

def test_invalid_link_almost_correct():
    """
    Test if the class raises exception for invalid link.
    """
    with pytest.raises(ImgurException):
        Imgur('http://.iimgur.com/jedEzFL')

def test_is_it_image_with_extension(single_image_i):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_i.is_it_image() == True

def test_is_it_image_without_extension_i(single_image_without_extension_i):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_without_extension_i.is_it_image() == True

def test_is_it_image_without_extension(single_image_without_extension):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_without_extension.is_it_image() == True

def test_is_it_album_image_with_extension(single_image_i):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_i.is_it_album() == False

def test_is_it_album_image_without_extension_i(single_image_without_extension_i):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_without_extension_i.is_it_album() == False

def test_is_it_album_image_without_extension(single_image_without_extension):
    """
    Test if the provided URL leads to an image or album.
    """
    assert single_image_without_extension.is_it_album() == False

def test_is_it_image_album_a(album_a):
    """
    Test if the provided URL leads to an image or album.
    """
    assert album_a.is_it_image() == False

def test_is_it_image_album_gallery(album_gallery):
    """
    Test if the provided URL leads to an image or album.
    """
    assert album_gallery.is_it_image() == False

def test_is_it_album_a(album_a):
    """
    Test if the provided URL leads to an image or album.
    """
    assert album_a.is_it_album() == True

def test_is_it_album_gallery(album_gallery):
    """
    Test if the provided URL leads to an image or album.
    """
    assert album_gallery.is_it_album() == True

def test_if_album_ends_with_grid_1(album_a):
    """
    Test if the provided link ends with '?grid'
    """
    assert album_a.is_it_grid() == False

def test_if_album_ends_with_grid_2(album_grid):
    """
    Test if the provided link ends with '?grid'
    """
    assert album_grid.is_it_grid() == True

def test_gallery_to_a(album_gallery, album_a):
    """
    Change /gallery/ to /a/
    """
    assert album_gallery.change_gallery() == album_a.url

def test_turn_album_into_grid(album_gallery, album_a, album_grid):
    """
    Turn album into grid.
    """
    assert album_gallery.turn_into_grid() == album_grid.url
    assert album_a.turn_into_grid() == album_grid.url
    assert album_grid.turn_into_grid() == album_grid.url

def test_raise_exception_turn_into_grid(single_image_i):
    """
    Raise exception if the provided link cannot be turned into grid.
    """
    with pytest.raises(ImgurException):
        single_image_i.turn_into_grid()

@pytest.mark.skip(reason='no way of currently testing this')
def test_get_image(single_image_without_extension):
    """
    Get a direct link to a single image.
    """
    result = deque({
        'url' : 'http://i.imgur.com/jedEzFL.jpg',
        'filename' : 'jedEzFL.jpg',
    })
    single_image_without_extension.prepare_images()
    assert single_image_without_extension.images == result

@pytest.mark.skip(reason='no way of currently testing this')
def test_get_images(album_gallery):
    """
    Get images from an album.
    """
    result = deque({
        'url' : 'http://i.imgur.com/lciC5G8.jpg',
        'filename' : 'lciC5G8.jpg',
    }, {
        'url' : 'http://i.imgur.com/6O1hqeY.jpg',
        'filename' : '6O1hqeY.jpg',
    })
    album_gallery.prepare_images()
    assert album_gallery.images == result

def test_contains_extension(single_image_i, single_image_without_extension):
    """
    Check if the extension is contained in image url.
    """
    assert single_image_i.contains_extension(single_image_i.url) == '.jpg'
    assert single_image_without_extension.contains_extension(
            single_image_without_extension.url
        ) == None

def test_get_image_filename(single_image_i):
    """
    Check if the method returns filename obtained from the direct image url.
    """
    assert single_image_i.get_image_filename(single_image_i.url) == 'jedEzFL.jpg'

def test_duplicates(single_image_without_extension, album_gallery):
    """
    Remove duplicates from matches returned from regex.
    """
    candidate_1 = [('jedEzFL', '.jpg'), ('jedEzFL', '.jpg')]
    candidate_2 = [('jedEzFL', '.jpg'), ('lciC5G8', '.jpg'),
                   ('jedEzFL', '.jpg'), ('lciC5G8', '.jpg')]
    assert single_image_without_extension.remove_duplicates(candidate_1) == [('jedEzFL', '.jpg')]
    assert album_gallery.remove_duplicates(candidate_2) == [('jedEzFL', '.jpg'), ('lciC5G8', '.jpg')]

def test_build_image_links(album_gallery):
    """
    Test if the input list of filename tuples returns direct links to images.
    """
    candidate = [('jedEzFL', '.jpg'), ('lciC5G8', '.jpg')]
    result = ['https://i.imgur.com/jedEzFL.jpg', 'https://i.imgur.com/lciC5G8.jpg']
    assert album_gallery.build_image_url_list(candidate) == result

def test_number_of_images(album_gallery):
    """
    Test the number of images contained in 'images' attribute.
    """
    assert album_gallery.number_of_images() == 0

def test_check_ordering(album_gallery):
    """
    Check if the image filenames have appended ordinal numbers.
    """
    candidates = deque([
        {'url' : 'https://i.imgur.com/jedEzFL.jpg', 'filename' : 'jedEzFL.jpg',},
        {'url' : 'https://i.imgur.com/lciC5G8.jpg', 'filename' : 'lciC5G8.jpg',},
    ])
    result = deque([
        {'url' : 'https://i.imgur.com/jedEzFL.jpg', 'filename' : '1-jedEzFL.jpg',},
        {'url' : 'https://i.imgur.com/lciC5G8.jpg', 'filename' : '2-lciC5G8.jpg',},
    ])

    album_gallery.images = candidates
    album_gallery.numerate_images()
    assert album_gallery.images == result

def test_digits_in_a_number(album_gallery):
    """
    Test to see how many digits are there in an album.
    """
    assert album_gallery.digits_in_a_number(7) == 1
    assert album_gallery.digits_in_a_number(12) == 2
    assert album_gallery.digits_in_a_number(1454) == 4
