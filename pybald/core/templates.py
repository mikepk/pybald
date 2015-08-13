#!/usr/bin/env python
# encoding: utf-8

import os
import unittest
from pybald.context import config
from mako.template import Template
from mako.lookup import TemplateLookup
import re
import logging

log = logging.getLogger(__name__)

# templates follow name.FORMAT.template so this is a simple
# regex check of that pattern
TEMPLATE_PATTERN = re.compile(r'([^\.]+)\.([^\.]+)\.template$')

class TemplateEngine(object):
    '''
    The basic template engine, looks up templates and renders them.
    Uses the mako template system
    '''

    def __init__(self, template_path=None, cache_path=None, helpers=None):
        # base template helpers all pybald projects have
        self.template_helpers = ['from pybald.core.helpers import img, link, humanize, js_escape, as_p',
                            'from pybald.core import page',
                            'from pybald.core.helpers import js_escape as js',
                            'from mako.filters import html_escape']

        if config.template_helpers:
            self.template_helpers.extend(config.template_helpers)

        # set the default filters to auto-html escape all content
        self.default_filters = ['h', 'unicode']
        if config.template_default_filters:
            self.default_filters = config.template_default_filters

        self.project_path = config.path

        try:
            default_template_path = os.path.join(os.path.dirname(
                                                os.path.realpath(__file__)),
                                                'default_templates')
            project_template_path = config.template_path or os.path.join(
                                                            self.project_path,
                                                            'app/views')
            project_cache_path = config.cache_path or os.path.join(
                                                           self.project_path,
                                                           'tmp/viewscache')
        except AttributeError:
            log.exception(("**Warning**\n"
                             "Unable to load templates from template path\n"
                             ))
            default_template_path = ""
            project_template_path = ""
            project_cache_path = ""

        fs_test = config.template_filesystem_check or config.debug or False
        self.lookup = TemplateLookup(directories=[project_template_path,
                                                  default_template_path],
                                     module_directory=project_cache_path,
                                     imports=self.template_helpers,
                                     input_encoding='utf-8',
                                     output_encoding='utf-8',
                                     filesystem_checks=fs_test,
                                     default_filters=self.default_filters)

    def form_render(self, template_name=None, format="form", **kargs):
        '''
        Render the form for a specific model using formalchemy.

        :param template_name: The name of the template to search for and
                              render for a form
        :param kargs: the data to render in the context of the form
                        template
        '''
        data = kargs
        try:
            template_id = kargs['fieldset'].template_id
        except (KeyError, AttributeError):
            template_id = 'forms/{0}'.format(template_name)

        mytemplate = self._get_template(template_id, format)
        # We use the render_unicode to return a native unicode
        # string for inclusion in another Mako template
        return mytemplate.render_unicode(**data)

    def _get_template(self, template, format="html"):
        '''
        Retrieves the proper template from the Mako template system.

        :param template: The name of the template in the filesystem to retrieve
                         for rendering.
        :param format: A string specifying the format for the template (html,
                       json, xml, etc...), overrides the format specified in
                       the data dictionary.

        The _get_template method of the template engine constructs a template
        name based on the template_id and the format and retrieves it from the
        Mako template system.
        '''
        # format can't be None, set to html as a default
        if format is None:
            format = 'html'
        if TEMPLATE_PATTERN.search(template):
            template_file = template
        else:
            template_file = "/{0}.{1}.template".format(template.lower().lstrip('/'),
                                                   format.lower())
        log.debug("Using template: {0}".format(template_file))
        # TODO: Add memc caching of rendered templates
        # also need to check if the internal caching is good enough
        return self.lookup.get_template(template_file)

    def __call__(self, template=None, data={}, format="html"):
        '''
        Renders the template.

        :param template: The name of the template in the filesystem to retrieve
                         for rendering.
        :param data: A dictionary that represents the context to render inside
                     the template. Keys in this dictionary will be available
                     to the template.
        :param format: A string specifying the format type to return (e.g. 'html',
                       'json', 'xml')

        Calls _get_template to retrieve the template and then renders it.
        '''
        template_data = dict(config.page_options.items() + data.items())
        mytemplate = self._get_template(template, format)
        log.debug("Rendering template")
        return mytemplate.render(**template_data)



class TemplateEngineTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
