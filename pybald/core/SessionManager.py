#!/usr/bin/env python
# encoding: utf-8
"""
SessionManager.py

Created by mikepk on 2009-07-06.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import datetime

from webob import Request, Response
from app.models.Session import Session

class SessionManager:
    '''Code to handle anonymous and user sessions, implemented as WSGI middleware.'''
    def __init__(self,application=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def process_session(self,environ,start_response):
        req = Request(environ)
        # check if the browser has a cookie with a session_id
        # load the session from the session_id
        try:
            session_id = req.cookies['session_id']
            environ['session'] = Session().load(session_id) 
            resp = req.get_response(self.application) #(environ, start_response)
        # no session_id cookie set, either no session
        # or create anon session
        except (KeyError, IOError, Session.NotFound):
            session_id = self.create_session()
            environ['session'] = self.session
            resp = req.get_response(self.application) #(environ, start_response)
            # modify the response object to add the cookie response
            self.create_session_cookie(resp)

        return resp(environ,start_response)

    def create_session(self):
        '''Create a new anonymous session.'''
        self.session = Session()
        self.session.generate_id()
        self.session.save()
        return self.session.session_id

    def create_session_cookie(self,resp):
        '''create the cookie for session storage, adds to a webob resp object'''
        # set cookies for testing
        #domain='' path, max_age, max_age=360 secure=True # https only
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=14)
        resp.set_cookie('session_id', self.session.session_id, expires=expires.strftime('%a, %d %b %Y %H:%M:%S UTC'), path='/') 
        resp.headers['Set-Cookie']
        return resp
        

class SessionManagerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()