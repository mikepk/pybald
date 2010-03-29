#!/usr/bin/env python
# encoding: utf-8
"""
ErrorController.py

Created by mikepk on 2009-07-25.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest
from pybald.core.BaseController import action, BaseController
from webob import Response

class ErrorController(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    @action
    def index(self,req):
        self.page['title'] = "We've encountered an error."
        return Response(body=self._view(), status=500)

    @action
    def not_found(self,req):
        self.page['title'] = "Page not found."
        return Response(body=self._view(), status=404)

    @action
    def not_authorized(self,req):
        self.page['title'] = "You're not allowed to see this."
        return Response(body=self._view(), status=401)

class ErrorControllerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()