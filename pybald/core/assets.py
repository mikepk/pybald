#!/usr/bin/env python
# encoding: utf-8

from lxml import etree

from webassets.env import Environment
from webassets import Bundle
from webassets.exceptions import BundleError
from pybald.core import page
import project
import os
from urlparse import urlparse

try:
    import pyhash
    hashfunc = pyhash.super_fast_hash()
except ImportError:
    hashfunc = hash

import logging
console = logging.getLogger(__name__)

# setting auto-build to false will keep all sub-nodes from
# running the XML parser.
env = Environment(os.path.join(project.path or '', "public"),
                  '',
                  debug=(not project.BUNDLE_ASSETS),
                  auto_build=bool(project.BUNDLE_AUTO_BUILD))


def _parse_bundle(elem, parent_bundle=None):
    '''Recursively generate webassets bundles by walking the xml tree'''
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
    attrib_dict['output'] = attrib_dict['output'].lstrip('/')
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
        '''
        Decorator that returns memoized responses.
        '''
        key = hashfunc(input_text)
        try:
            return self.cached[key]
        except KeyError:
            self.cached[key] = self.method(input_text)
            return self.cached[key]


@memoize_bundles
def bundle(input_text):
    '''
    Parse XML fragments from a string looking for asset bundles and
    process them into webasset bundles.
    '''
    # XML parse the fragments
    output_buffer = []
    xml_fragment = u'''<fragments>{0}</fragments>'''.format(input_text)
    root = etree.fromstring(xml_fragment)
    for elem in root:
        # parse all bundles
        if elem.tag == 'bundle':
            bundle_tag = elem
            bundle, asset_type = _parse_bundle(bundle_tag)
            # every asset type has a default 'link type'
            link_func = getattr(page, 'add_{0}'.format(asset_type))
            # construct the asset urls
            try:
                assets = [link_func(url) for url in bundle.urls(env=env)]
            except BundleError as err:
                console.exception("Problem bundling.")
                console.warning("!"*80 + '''
  Warning, missing pre-compiled static assets. Switching to debug mode
  automatically. Run compile_static_assets.py to pre-create the compiled
  minified static assets.
''' + "!"*80)
                env.debug = True
                assets = [link_func(url) for url in bundle.urls(env=env)]
            output_buffer.extend(assets)
            # add any text nodes that got glommed onto
            # the node
            if bundle_tag.tail is not None:
                output_buffer.append(bundle_tag.tail)
        # just dump out anything that's not a bundle
        else:
            output_buffer.append(etree.tostring(elem, method="html"))
    return u'\n'.join([unicode(item) for item in output_buffer])
