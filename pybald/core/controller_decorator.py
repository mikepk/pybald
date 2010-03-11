#!/usr/bin/env python
# encoding: utf-8
"""
controller_decorator.py

Some syntactic sugar to make WSGI controllers a little
less cumbersome. This was lifted and modified from the WSGI docs
'roll your own web framework' section.

Created by mikepk on 2009-06-30.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

from webob import Request, Response
from webob import exc

from SessionManager import SessionManager
import re

# action / method decorator
def action(func):
    def replacement(self, environ, start_response):
        req = Request(environ)
        # this code defines the template id to match against
        # template path = controller name + '/' + action name (except in the case of)
        # index
        self.template_id = re.search('(\w+)Controller',self.__module__).group(1).lower()
        if not re.search('index',func.__name__):
            self.template_id += '/'+str(func.__name__)

        # add any url variables as members of the controller
        if req.urlvars:
            ignore = ['controller','action']
            for key in req.urlvars.keys(): # and not in ignore:
                #if key not in ignore:
                setattr(self,key,req.urlvars[key])

        # run the controllers "pre" code
        resp = self._pre(req)
        
        # If the pre code returned a response, return that
        if not resp:
            try:
                resp = func(self,req)
            except exc.HTTPException, e:
                resp = e

        # if there's no return, call the view method
        if not resp:
            resp = self._view()

        # if the function returns a string
        # wrap it in a response object
        if isinstance(resp, basestring):
            resp = Response(body=resp)

        # run the controllers post code
        self._post(req,resp)
        return resp
    return replacement

# I may remove this, using action exclusively
# since controllers are no longer callable
controller = action