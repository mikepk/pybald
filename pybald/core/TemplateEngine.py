#!/usr/bin/env python
# encoding: utf-8
"""
TemplateEngine.py

Created by mikepk on 2009-06-29.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import project

from mako.template import Template
from mako.lookup import TemplateLookup

class TemplateEngine:
    '''The basic template engine, looks up templates and renders them. Uses the mako template system'''
            
    def __init__(self, template_path=None): 
        self.project_path = project.get_path()
        default_template_path = os.path.join( os.path.dirname( os.path.realpath(__file__) ), 'default_templates' )
        fs_test = project.template_filesystem_check or project.debug or False

        project_template_path = template_path or os.path.join(self.project_path,'app/views')

        self.lookup = TemplateLookup(directories=[project_template_path, default_template_path], 
            module_directory=os.path.join(self.project_path,'viewscache'),
            imports=[
                'from pybald.core.helpers import link, img, humanize',
                ],
                input_encoding='utf-8', output_encoding='utf-8',
                filesystem_checks=fs_test)


    def form_render(self, template_name=None, **kargs):
        '''Render the form for a specific model using formalchemy.'''
        data = kargs
        try:
            data['template_id'] = kargs['fieldset'].template_id
        except (KeyError, AttributeError):
            data['template_id'] = 'forms/%s' % template_name

        # get passed in form if it's in the data
        # but more likely we'll use the form extension
        format = data.get("format", None) or "form"

        mytemplate = self._get_template(data, format)
        # We use the render_unicode to return a native unicode
        # string for inclusion in another Mako template
        return mytemplate.render_unicode(**data)

    
    def _get_template(self, data, format=None):
        # if the data dictionary has a format, use that, 
        # otherwise default to the passed in value or html
        format = format or data.get("format", None) or "html"

        # TODO: Add memc caching of rendered templates
        # also need to check if the internal caching is good enough
        return self.lookup.get_template("/%s.%s.template" % (data['template_id'].lower(), format.lower()))

    
    def __call__(self, data, format=None):
        '''Callable method that executes the template.'''
        mytemplate = self._get_template(data, format)
        return mytemplate.render(**data)



engine = TemplateEngine()

class TemplateEngineTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()