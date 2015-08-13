#!/usr/bin/env python
# encoding: utf-8
from lxml import html

from webassets.env import Environment
from webassets import Bundle
from webassets.exceptions import BundleError
from pybald.core import page
from pybald.asset_filters.jsx import JsxFilter
from webassets.filter import register_filter

from pybald import context
import os
from urlparse import urlparse

# add custom JsxFilter
register_filter(JsxFilter)

try:
    import pyhash
    hashfunc = pyhash.super_fast_hash()
except ImportError:
    hashfunc = hash

import logging
log = logging.getLogger(__name__)

# python 3
try:
    type(unicode)
except NameError:
    unicode = str

public_path = os.path.join(context.config.path or '', "public")

# set the bundle input and output paths
if context.config.BUNDLE_OUTPUT_PATH:
    bundle_output_path = context.config.BUNDLE_OUTPUT_PATH
else:
    bundle_output_path = ''

if context.config.BUNDLE_SOURCE_PATHS:
    bundle_input_paths = [os.path.join(context.config.path or '', path.lstrip('/'))
                            for path in context.config.BUNDLE_SOURCE_PATHS]
else:
    bundle_input_paths = [public_path]

cache_path = os.path.join(context.config.path or '', 'tmp', '.webassets-cache')
manifest_file = os.path.join(context.config.path or '', 'tmp', '.webassets-manifest')

# auto create cache path if not present
if not os.path.exists(cache_path):
    os.makedirs(cache_path)

# setting auto-build to false will keep all sub-nodes from
# running the XML parser.
env = Environment(public_path,
                  url='',
                  debug=(not context.config.BUNDLE_ASSETS),
                  auto_build=bool(context.config.BUNDLE_AUTO_BUILD),
                  load_path=bundle_input_paths,
                  cache=cache_path,
                  manifest="".join(["json:", manifest_file]),
                  # Take any bundle filter options and apply them to the config
                  **(context.config.BUNDLE_FILTER_OPTIONS or {}))

def _parse_bundle(elem, parent_bundle=None):
    '''Recursively generate webassets bundles by walking the xml/html tree'''
    if elem.tag != "bundle":
        raise SyntaxError("Bundling only works with bundle tags.")
    contents = []
    asset_type = None
    asset_types = []
    # get all sub_bundles and process them
    for t in elem:
        if t.tag == 'bundle':
            bundle, asset_type = _parse_bundle(t)
            contents.append(bundle)
        elif t.tag == 'link':
            file_path = urlparse(t.attrib.get('href', '')).path
            contents.append(file_path.lstrip('/'))
            asset_types.append('css')
        elif t.tag == 'script':
            file_path = urlparse(t.attrib.get('src', '')).path
            contents.append(file_path.lstrip('/'))
            asset_types.append('js')
    if not asset_types:
        raise SyntaxError("No assets found in the bundle tag. Include javascript, css, or source files in the bundle.")
    elif len(set(asset_types)) > 1:
        raise SyntaxError("All assets in a bundle must be of the same type. They should all be javascript, css etc... or compiled to the same asset type.")
    asset_type = asset_types[0]

    attrib_dict = dict(**elem.attrib)
    # convert text True/False to boolean
    if 'debug' in attrib_dict:
        if attrib_dict['debug'] == 'True':
            attrib_dict['debug'] = True
        elif attrib_dict['debug'] == 'False':
            attrib_dict['debug'] = False

    # default temporary output file, just the version as name...
    if 'output' not in attrib_dict:
        attrib_dict['output'] = '/min/{0}/%(version)s.{0}'.format(asset_type)

    # remove leading slashes since webassets works on relative paths
    # a little hacky but keeps the document (web page) syntax cleaner
    attrib_dict['output'] = os.path.join(bundle_output_path, attrib_dict['output'].lstrip('/')).lstrip('/')
    new_bundle = Bundle(*contents, **attrib_dict)
    return new_bundle, asset_type


class memoize_bundles(object):
    '''
    Store the result of the XML parse and return it on subsequent
    requests.
    '''
    def __init__(self, method):
        self.method = method
        self.cached = {}

    def __call__(self, input_text):
        if context.config.debug:
            return self.method(input_text)
        key = hashfunc(input_text)
        try:
            return self.cached[key]
        except KeyError:
            self.cached[key] = self.method(input_text)
            return self.cached[key]


@memoize_bundles
def bundle(input_text):
    '''
    Parse HTML/XML fragments from a string looking for asset bundles and
    process them into webasset bundles.
    '''
    # HTML/XML parse the fragments
    output_buffer = []
    html_fragment = u'''<div>{0}</div>'''.format(input_text)
    root = html.fragment_fromstring(html_fragment)

    for elem in root:
        # parse all bundles
        if elem.tag == 'bundle':
            bundle_tag = elem
            bundle, asset_type = _parse_bundle(bundle_tag)

            # every asset type has a default 'link type'
            link_func = getattr(page, 'add_{0}'.format(asset_type))
            with bundle.bind(env):
                assets = [link_func(url) for url in bundle.urls()]
            output_buffer.extend(assets)
            # add any text nodes that got glommed onto
            # the node
            if bundle_tag.tail is not None:
                output_buffer.append(bundle_tag.tail)
        # just dump out anything that's not a bundle
        else:
            output_buffer.append(html.tostring(elem))
    return u'\n'.join([unicode(item) for item in output_buffer])
