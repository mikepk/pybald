#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

import datetime

from webob import Request, Response

import re

class SessionManager(object):
    '''Code to handle anonymous and user sessions, implemented as WSGI middleware.'''

    def __init__(self, application=None, days=14, session_class=None):
        self.session_class = session_class
        self.days = days
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self, environ, start_response):
        req = Request(environ)

        environ['pybald.session'] = self.session_class._before(req)

        # update or create the pybald.extension to populate controller instances
        environ['pybald.extension'] = environ.get('pybald.extension', {})
        environ['pybald.extension']['session'] = environ['pybald.session']

        # call the next part of the pipeline
        resp = req.get_response(self.application)

        # execute any post-processing code for the session
        # this includes saving the session if necessary.
        environ['pybald.session']._after(req, resp)

        return resp(environ,start_response)

