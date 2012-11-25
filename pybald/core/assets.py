#!/usr/bin/env python
# encoding: utf-8

from lxml import etree

from webassets.env import Environment
from webassets import Bundle
from pybald.core import page
import project
import os
from urlparse import urlparse

env = Environment(os.path.join(project.path or '', "public"),
                  '',
                  debug=project.debug)


class AssetBundleSyntaxError(Exception):
    pass


def _parse_bundle(elem, parent_bundle=None):
    '''Recursively generate webassets bundles by walking the xml tree'''
    if elem.tag != "bundle":
        raise AssetBundleSyntaxError("Bundling only works with bundle tags.")
    contents = []
    # get all sub_bundles and process them
    for t in elem:
        if t.tag == 'bundle':
            contents.append(_parse_bundle(t))
        elif t.tag == 'link':
            file_path = urlparse(t.attrib.get('href', '')).path
            contents.append(file_path.lstrip('/'))
        elif t.tag == 'script':
            file_path = urlparse(t.attrib.get('src', '')).path
            contents.append(file_path.lstrip('/'))

    attrib_dict = dict(**elem.attrib)
    attrib_dict.pop('asset_type', None)
    # convert text True/False to boolean
    if 'debug' in attrib_dict:
        if attrib_dict['debug'] == 'True':
            attrib_dict['debug'] = True
        elif attrib_dict['debug'] == 'False':
            attrib_dict['debug'] = False
    # remove leading slashes since webassets works on relative paths
    # a little hacky but keeps the document (web page) syntax cleaner
    attrib_dict['output'] = attrib_dict['output'].lstrip('/')
    new_bundle = Bundle(*contents, **attrib_dict)
    return new_bundle


def bundle(input_text):
    '''
    Parse XML fragments from a string looking for asset bundles and
    process them into webasset bundles.
    '''
    # XML parse the fragments
    string_buffer = []
    xml_template = u'''<fragments>{0}</fragments>'''
    root = etree.fromstring(xml_template.format(input_text))
    for elem in root:
        if elem.tag == 'bundle':
            bundle_tag = elem
            bundle = _parse_bundle(bundle_tag)
            # every asset type has a default 'template'
            asset_type = bundle_tag.attrib.get('asset_type', 'add_js')
            link_func = getattr(page, asset_type)
            # construct the asset urls
            assets = [link_func(url) for url in bundle.urls(env=env)]
            string_buffer.extend(assets)
            if bundle_tag.tail is not None:
                string_buffer.append(bundle_tag.tail)
        else:
            string_buffer.append(etree.tostring(elem))
    return ''.join([unicode(item) for item in string_buffer])
