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
# import core
import project
from mako.template import Template
from mako.lookup import TemplateLookup

class TemplateEngine:
    '''The basic template engine, looks up templates and renders them. Uses the mako template system'''
    def __init__(self): #,project_path=project.path): #'/usr/share/enerd/template_project'):
        pass
        
    def __call__(self,data,format="html"):
        path = project.get_path()
        mylookup = TemplateLookup(directories=[path+'/app/views'], module_directory=path+'/viewscache',
        imports=['from routes import url_for','from pybald.core.helpers import link_to','from pybald.core.helpers import link_img_to'],input_encoding='utf-8',output_encoding='utf-8')
        mytemplate = mylookup.get_template("/"+data['template_id'].lower()+"."+format.lower()+".template")
        return mytemplate.render(**data)

class TemplateEngineTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()