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

        # if new_session:
        #     # modify the response object to add the cookie response
        #     self.create_session_cookie(req, resp)

        # execute any post-processing code for the session
        # this includes saving the session if necessary.
        environ['pybald.session']._after(req, resp)

        return resp(environ,start_response)

#     def create_session(self,environ):
#         '''Create a new anonymous session.'''
#         environ['pybald.session'] = self.session_class()
#         # mc.set('session_id:{0}'.format(self.session_id), self)
#         #environ['pybald.session'].save().flush()
#         return environ['pybald.session'].session_id
# 
#     def create_session_cookie(self, req, resp):
#         '''create the cookie for session storage, adds to a webob resp object'''
#         # set cookies for testing
#         #domain='' path, max_age, max_age=360 secure=True # https only
#         expires=None
#         if self.days:
#             expires = datetime.timedelta(days=self.days)
#         # resp.set_cookie('session_id', self.session.session_id, expires=expires.strftime('%a, %d %b %Y %H:%M:%S UTC'), path='/')
#         resp.set_cookie('session_id', req.environ['pybald.session'].session_id, max_age=expires, path='/')
#         return resp
# 
# 
# class SessionManagerTests(unittest.TestCase):
#     def setUp(self):
#         pass
# 
# 
# if __name__ == '__main__':
#     unittest.main()