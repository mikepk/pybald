#!/usr/bin/env python
# encoding: utf-8
'''HTML page helper functions as well as simple asset tag handling.'''

import os
import project

# from urlparse import urlparse, ParseResult
# global request_config... how can we eliminate?
# from routes import request_config
from pybald.core.helpers import HTMLLiteral, AssetUrl

import logging
console = logging.getLogger(__name__)
try:
    import pyhash
    hashfunc = pyhash.super_fast_hash()
except ImportError:
    console.warn("!"*10 + '''  Using python built-in hash() for asset URL
generation. This is system implementation specific and may result in different
hosts mapping static assets to different static hosts. That may cause
inefficient use of browser caches. Optionally you can install pyhash to
install additional fast, non-cryptographic, hashes that are not system
dependent.

pip install pyhash
''')
    hashfunc = hash



asset_tag_cache = {}


def compute_asset_tag(filename, pattern='{filename}{extension}?v={tag}'):
    asset_tag = asset_tag_cache.get(filename, None)
    try:
        if not asset_tag:
            asset_tag = str(
                int(round(os.path.getmtime(os.path.join(project.path,
                                                        "public",
                                                        filename.lstrip("/"))))
                ))
        asset_tag_cache[filename] = asset_tag
    except OSError:
        asset_tag_cache[filename] = "xxx"
    filename, ext = os.path.splitext(filename)
    return pattern.format(filename=filename, tag=asset_tag, extension=ext)


def add_js(filename):
    return HTMLLiteral('''<script src="{0}"></script>'''.format(
                                        AssetUrl(compute_asset_tag(filename))))


def add_css(filename, media="screen"):
    return HTMLLiteral(('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                AssetUrl(compute_asset_tag(filename)),
                                                str(media)))


def add_extern_css(filename, media="screen"):
    return HTMLLiteral(('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                filename,
                                                str(media)))


