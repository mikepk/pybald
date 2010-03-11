#!/usr/bin/env python
# encoding: utf-8
"""
BaseController.py

Base Controller that all PyBald controllers inherit from.

Created by mikepk on 2009-06-29.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

from pybald.core.TemplateEngine import TemplateEngine

from webob import Request, Response
from webob import exc
import re

# action / method decorator
# This decorator takes in the action method and adds some syntactic sugar around it.
# Allows the actions to work with WebOb request respons objects, and handles default
# behaviors, such as displaying the view when nothing is returned, or plain text
# if a string is returned.
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

        return resp(environ, start_response)
    return replacement


class BaseController():
    '''Base controller that includes the view and a default index method.'''
    def __init__(self):
        '''Initialize the base controller with a page object. Page dictionary controls title, headers, etc...'''
        self.page = {'title':None,'metas':[],'headers':[]}
                
    @action
    def index(self,req):
        '''default index action'''
        pass
        
    def _pre(self,req):
        '''Code to run before any action.'''
        try:
            # set the session and user
            # This will except in all cases where the session manager is not used
            self.session = req.environ['session']
            try:
                self.user = self.session.cachestore['user']
            except KeyError:
                self.user = None

            # check and clear the session error state.
            # The next handler should handle the error or it's lost.
            try:
                if self.session.cachestore["error"]:
                    self.error = self.session.cachestore["error"]
                    self.session.cachestore["error"] = None
                    self.session.save()
            except KeyError:
                self.error = None

        except KeyError:
            self.session = None
            self.user = None
            self.error = None

    def _post(self,req,resp):
        '''Code to run after any action.'''
        pass

    def _view(self,user_dict=None):
        '''Method to invoke the template engine and display a view'''
        view = TemplateEngine()
        # user supplied dictionary, otherwise create a dictionary
        # from the controller
        if user_dict:
            user_dict['template_id'] = self.template_id
            return view(user_dict)
        # View has access to all the internal attributes
        # inside the view (for Mako at least) the dictionary is copied
        else:
            return view(self.__dict__)
        
class BaseControllerTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()