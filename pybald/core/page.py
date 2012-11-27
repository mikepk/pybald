#!/usr/bin/env python
# encoding: utf-8
'''HTML page helper functions as well as simple asset tag handling.'''

import os
import project

from urlparse import urlparse, ParseResult
# from routes import url_for
from routes import request_config


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
        if (project.USE_CDN and project.CDN_HOST) or not project.debug:
            # host_num = hash(self.raw_url) % len(project.STATIC_HOSTS)
            # host = project.STATIC_HOSTS[host_num]
            # self['netloc'] = host
            self['netloc'] = project.CDN_HOST
        if self['netloc'] and not self['scheme']:
            # get the protocol for the current request
            self['scheme'] = request_config().protocol
        return ParseResult(**self).geturl()


asset_tag_cache = {}


def compute_asset_tag(filename):
    asset_tag = asset_tag_cache.get(filename, None)
    try:
        if not asset_tag:
            asset_tag = str(
                int(
                   round(os.path.getmtime(
                    os.path.join(project.path, "public", filename.lstrip("/")))
                    )
                ))
        asset_tag_cache[filename] = asset_tag
    except OSError:
        asset_tag_cache[filename] = "xxx"
    return "?v={0}".format(asset_tag)


def add_js(filename):
    return '''<script type="text/javascript" src="{0}"></script>'''.format(
                                                AssetUrl(filename),
                                                # filename,
                                                compute_asset_tag(filename))


def add_css(filename, media="screen"):
    return ('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                AssetUrl(filename),
                                                # filename,
                                                str(media),
                                                compute_asset_tag(filename))


def add_extern_css(filename, media="screen"):
    return ('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet" />''').format(
                                                filename,
                                                # filename,
                                                str(media),
                                                compute_asset_tag(filename))
