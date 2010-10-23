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

from pybald.core.TemplateEngine import engine

from webob import Request, Response
from webob import exc
import re

from pybald.db.models import db

from routes import redirect_to

# action / method decorator
# This decorator takes in the action method and adds some syntactic sugar around it.
# Allows the actions to work with WebOb request / response objects, and handles default
# behaviors, such as displaying the view when nothing is returned, or plain text
# if a string is returned.
def action(func):
    def replacement(self, environ, start_response):
        req = Request(environ)
        # this code defines the template id to match against
        # template path = controller name + '/' + action name (except in the case of)
        # index

        self.template_id = re.search('(\w+)Controller',self.__module__).group(1).lower()
        # 'index' is a special name. The index action maps to the controller name (no action view)
        if not re.search(r'index|__call__',func.__name__):
            self.template_id += '/'+str(func.__name__)

        # add any url variables as members of the controller
        # TODO: setup a way to avoid collisions with existing members (data overriding view, 
        # possible sec hole)
        if req.urlvars:
            for key in req.urlvars.keys():
                #Set the controller object to contain the url variables
                # parsed from the dispatcher / router
                setattr(self,key,req.urlvars[key])
        # run the controllers "pre" code
        # resp = self._pre(req)
        # # If the pre code returned a response, return that
        # if not resp:
        resp = self._pre(req) or func(self,req)

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
    replacement.__name__ = func.__name__
    return replacement


class BaseController():
    '''Base controller that includes the view and a default index method.'''
    def __init__(self):
        '''Initialize the base controller with a page object. Page dictionary controls title, headers, etc...'''
        self.page = {'title':None,'metas':[],'headers':[]}
        self.error = None
        self.user = None
        self.session = None
                
    @action
    def index(self,req):
        '''default index action'''
        pass
        
    def _pre(self,req):
        '''Code to run before any action.'''
        pass
        # try:
        #     # set the session and user
        #     # This will except in all cases where the session manager is not used
        #     self.session = req.environ['pybald.session']
        #     try:
        #         self.user = self.session.user
        #     except (AttributeError,KeyError):
        #         self.user = None
        # 
        #     # # check and clear the session error state.
        #     # # The next handler should handle the error or it's lost.
        #     # try:
        #     #     if self.session.cache:
        #     #         if self.session.cache["error"]:
        #     #             self.error = self.session.cache["error"]
        #     #             self.session.cache["error"] = None
        #     #             self.session.save(True)
        #     #     else:
        #     #         self.error = None
        #     # except KeyError:
        #     #     self.error = None
        # 
        # except KeyError:
        #     self.session = None
        #     self.user = None
        #     self.error = None

    def _post(self,req,resp):
        '''Code to run after any action.'''
        # Closes the db Session object. Required to avoid holding sessions
        # indefinitely and overruning the sqlalchemy pool
        db.remove()
        # pass

    def _redirect_to(self,url):
        '''Redirect the controller'''
        return redirect_to(url)

    def _view(self,user_dict=None):
        '''Method to invoke the template engine and display a view'''
        view = engine
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