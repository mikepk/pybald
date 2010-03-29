#!/usr/bin/env python
# encoding: utf-8
"""
HomeController.py

Created by mikepk on 2009-06-28.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from pybald.core.BaseController import action, BaseController

class HomeController(BaseController):
    '''A simple controller object'''

    @action
    def index(self,req):
        self.message = "Hello, World!"

class HomeControllerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()