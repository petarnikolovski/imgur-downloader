# What is this?

This is imgur downloader. It can download a single image, album, or gallery.

## How to use?

```python
python3 crawlgur.py -v https://imgur.com/a/album_id /path/to/directory
```

Types of links that are allowed:

* http(s)://i.imgur.com/[image_hash].[extension]
* http(s)://i.imgur.com/[image_hash]
* http(s)://imgur.com/[image_hash]
* http(s)://imgur.com/a/[album_hash]
* http(s)://imgur.com/gallery/[album_hash]

Additional documentation is available in the source code itself.

# TODO

* Download user albums e.g. [username].imgur.com
