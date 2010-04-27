#!/usr/bin/env python
# encoding: utf-8
"""
BaseForm.py

Created by mikepk on 2010-04-25.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from formalchemy import FieldSet

import project
from formalchemy import templates, config
from pybald.core.TemplateEngine import engine

# set the Pybald Mako engine to be the main
# form template engine
config.engine = engine.form_render

class BaseForm(FieldSet):
    def __init__(self,instance=None, data=None):
        FieldSet.__init__(self,instance or self.__class__, data=data or None)
        # set the template_id to the name of the model
        self.template_id = os.path.join('forms',self.model.__class__.__name__.lower())
        
class BaseFormTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()