#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

import project

from mako.template import Template
from mako.lookup import TemplateLookup

# base tempalte helpers all pybald projects have
template_helpers = ['from pybald.core.helpers import img, link, humanize, js_escape, as_p',
                    'from pybald.core.helpers import js_escape as js',
                    'from mako.filters import html_escape']

if project.template_helpers:
    template_helpers.extend(project.template_helpers)

class TemplateEngine:
    '''
    The basic template engine, looks up templates and renders them.
    Uses the mako template system
    '''

    def __init__(self, template_path=None, cache_path=None):
        self.project_path = project.path
        try:
            default_template_path = os.path.join( os.path.dirname(
                                                    os.path.realpath(__file__)
                                                      ), 'default_templates' )
            project_template_path = template_path or os.path.join(
                                                self.project_path,'app/views')
            project_cache_path = cache_path or os.path.join(
                                               self.project_path,'viewscache')
        except AttributeError, e:
            sys.stderr.write(("**Warning**\n"
                             "Exception: {exception}\n"
                             "Unable to load templates from template path\n"
                             ).format(exception=e))
            default_template_path = ""
            project_template_path = ""
            project_cache_path = ""

        fs_test = project.template_filesystem_check or project.debug or False

        self.lookup = TemplateLookup(directories=[project_template_path,
                                                  default_template_path],
                                     module_directory=project_cache_path,
                                     imports=template_helpers,
                                     input_encoding='utf-8',
                                     output_encoding='utf-8',
                                     filesystem_checks=fs_test)


    def form_render(self, template_name=None, **kargs):
        '''
        Render the form for a specific model using formalchemy.

        :param template_name: The name of the template to search for and
                              render for a form
        :param **kargs: the data to render in the context of the form
                        template
        '''
        data = kargs
        try:
            data['template_id'] = kargs['fieldset'].template_id
        except (KeyError, AttributeError):
            data['template_id'] = 'forms/{0}'.format(template_name)

        # get passed in form if it's in the data
        # but more likely we'll use the form extension
        format = data.get("format", None) or "form"

        mytemplate = self._get_template(data, format)
        # We use the render_unicode to return a native unicode
        # string for inclusion in another Mako template
        return mytemplate.render_unicode(**data)


    def _get_template(self, data, format=None):
        '''
        Retrieves the proper template from the Mako template system.

        :param data: A dictionary containing the ``template_id`` and ``format``
                     for the template lookup.
        :param format: A string specifying the format for the template (html,
                       json, xml, etc...), overrides the format specified in
                       the data dictionary.

        The _get_template method of the template engine constructs a template
        name based on the template_id and the format and retrieves it from the
        Mako template system.
        '''
        # if the data dictionary has a format, use that,
        # otherwise default to the passed in value or html
        format = format or data.get("format", None) or "html"

        # TODO: Add memc caching of rendered templates
        # also need to check if the internal caching is good enough
        return self.lookup.get_template("/{0}.{1}.template".format(data['template_id'].lower(), format.lower()))


    def __call__(self, data, format=None):
        '''
        Renders the template.

        :param data: A dictionary that represents the context to render inside
                     the template. Items in this dictionary will be available
                     to the template.
        :param format: A string specifying the format type to return, this
                       overrides a format specified in the data dictionary

        Calls _get_template to retrieve the template and then renders it.
        '''
        mytemplate = self._get_template(data, format)
        return mytemplate.render(**data)

#module scope singleton, should this be changed?
engine = TemplateEngine()

class TemplateEngineTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()
