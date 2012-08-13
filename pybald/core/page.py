#!/usr/bin/env python
# encoding: utf-8
'''HTML page helper functions as well as simple asset tag handling.'''

import os
import project

# singleton asset_tag_cache
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
    return '''<script type="text/javascript" src="{0}{1}"></script>'''.format(
                                                filename,
                                                compute_asset_tag(filename) )

def add_css(filename, media="screen"):
    return '''<link type="text/css" href="{0}{2}" media="{1}" rel="stylesheet" />'''.format(
                                                filename,
                                                str(media),
                                                compute_asset_tag(filename) )
