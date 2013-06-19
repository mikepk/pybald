#!/usr/bin/env python
# encoding: utf-8
'''HTML page helper functions as well as simple asset tag handling.'''

import os
import project
import re

from urlparse import urlparse, ParseResult
from routes import request_config

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


# parse result keys
class AssetUrl(dict):
    '''Wraps urls and returns URL transformations when necessary. Examples
    include when running static assets on a CDN.
    '''
    keys = ("scheme", "netloc", "path", "params", "query", "fragment")

    def __init__(self, url):
        self.raw_url = url
        super(AssetUrl, self).__init__(**dict(zip(self.keys, urlparse(url))))

    def __str__(self):
        '''Return a transformed URL if necessary (appending protocol and CDN)'''
        if self.get('netloc', None):
            # Don't CDN urls with hosts
            return self.raw_url
        if (project.USE_CDN and (project.CDN_HOST or project.STATIC_HOSTS)):
            protocol = request_config().protocol
            if protocol is not "https" and project.STATIC_HOSTS:
                self['netloc'] = project.STATIC_HOSTS[hashfunc(self.raw_url) %
                                                      len(project.STATIC_HOSTS)]
            else:
                self['netloc'] = project.CDN_HOST
            if self['netloc'] and not self['scheme']:
                # get the protocol for the current request
                # this requires the custom HTTP header X-Forwarded-Proto
                # set if running behind a proxy (or if SSL is terminated
                # upstream)
                self['scheme'] = request_config().protocol
        return ParseResult(**self).geturl()


asset_tag_cache = {}


def compute_asset_tag(filename, pattern='{filename}.sv{tag}x{extension}'):
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
    return '''<script type="text/javascript" src="{0}"></script>'''.format(
                                        AssetUrl(compute_asset_tag(filename)))


def add_css(filename, media="screen"):
    return ('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                AssetUrl(compute_asset_tag(filename)),
                                                str(media))


def add_extern_css(filename, media="screen"):
    return ('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                filename,
                                                str(media))
