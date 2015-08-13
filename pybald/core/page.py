#!/usr/bin/env python
# encoding: utf-8
'''HTML page helper functions as well as simple asset tag handling.'''

import os
from pybald import context
from pybald.core.helpers import HTMLLiteral, AssetUrl
import logging
log = logging.getLogger(__name__)

# TODO - this singleton should be replaced
asset_tag_cache = {}

def compute_asset_tag(filename, pattern='{filename}{extension}?v={tag}'):
    '''
    Create a unique signature for a file.

    This asset tag is used for cache busting.
    '''
    asset_tag = asset_tag_cache.get(filename, None)
    try:
        if not asset_tag:
            asset_tag = str(
                int(round(os.path.getmtime(os.path.join(context.config.path,
                                                        "public",
                                                        filename.lstrip("/"))))
                ))
        asset_tag_cache[filename] = asset_tag
    except OSError:
        asset_tag_cache[filename] = "xxx"
    filename, ext = os.path.splitext(filename)
    return pattern.format(filename=filename, tag=asset_tag, extension=ext)


def add_js(filename):
    '''Add a script tag to a template.

    This helper function is also config aware and will re-write asset urls
    based on CDN and other rules.'''
    return HTMLLiteral('''<script src="{0}"></script>'''.format(
                                        AssetUrl(compute_asset_tag(filename))))


def add_css(filename, media="screen"):
    '''Add a link/css tag to a template.

    This helper function is also config aware and will re-write asset urls
    based on CDN and other rules.'''
    return HTMLLiteral('''<link type="text/css" href="{0}" media="{1}" rel="stylesheet">'''.format(
                                                AssetUrl(compute_asset_tag(filename)),
                                                str(media)))


def add_extern_css(filename, media="screen"):
    return HTMLLiteral(('''<link type="text/css" href="{0}"'''
            ''' media="{1}" rel="stylesheet">''').format(
                                                filename,
                                                str(media)))


