#!/usr/bin/env python
# encoding: utf-8
"""
ErrorController.py

Created by mikepk on 2012-09-06.
Copyright (c) 2012 Michael Kowalchik. All rights reserved.
"""

import os
import unittest
from pybald.core.controllers import action, BaseController, render_view
from webob import Response
from mako import exceptions

import project
from collections import defaultdict

def error_response(template="general_error", status_code=500):
    template = os.path.join('error', template)
    return Response(body=render_view(template=template, format="html"),
                            status=status_code)

class ErrorController(BaseController):
    '''Controller to handle error exceptions.'''
    # map status codes to error controller actions
    error_map = defaultdict(lambda:'general_error',
                                    {404:'not_found',
                                     410:'gone',
                                     401:'not_authorized',
                                     500:'general_error'})


    def __init__(self, *pargs, **kargs):
        '''Setup the error controller'''
        self.status_code = kargs.pop('status_code', 500)
        self.message = kargs.pop('message', None)
        super(ErrorController, self).__init__(*pargs, **kargs)


    @action
    def http_client_error(self, req):
        '''A normal, non-code, http error'''
        try:
            return error_response(self.error_map[self.status_code],
                                  self.status_code)
        except Exception, err:
            return error_response('general_error', self.status_code)

    @action
    def __call__(self, req):
        '''
        The ErrorController will return a formatted stack trace if in debug
        mode, or point to the regular error page otherwise.
        '''
        if project.email_errors or project.debug:
            stack_trace = render_view(template='stack_trace', data={'req':req})

        if project.debug:
            return Response(body=stack_trace, status=self.status_code)
        else:
            return error_response('general_error', self.status_code)


class ErrorControllerTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()