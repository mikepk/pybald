#!/usr/bin/env python
# encoding: utf-8
# """
# BaseController.py
# 
# Base Controller that all PyBald controllers inherit from.
# 
# Created by mikepk on 2009-06-29.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.
# """

import sys
import os
import unittest

import os.path

from pybald.core.templates import engine

from webob import Request, Response
from webob import exc
import re

from pybald.db.models import session
from pybald.util import camel_to_underscore

from routes import redirect_to
import project
media_version = project.media_version
project_path = project.get_path()
page_options = project.page_options

from pybald.db import models

# action / method decorator
# This decorator takes in the action method and adds some syntactic sugar around it.
# Allows the actions to work with WebOb request / response objects, and handles default
# behaviors, such as displaying the view when nothing is returned, or plain text
# if a string is returned.
def action(method):
    '''
    Decorates methods to turn them into pybald-style actions.

    :param method: The method to turn into a pybald-style action.

    This decorator takes the method of a controller instance (or any method that is a WSGI app) 
    and adds some syntactic sugar around it to allow the method to use WebOb Request, 
    Response objects.
    
    It allows actions to work with WebOb request / response objects, and handles default
    behaviors, such as displaying the view when nothing is returned, or setting up a plain text
    Response if a string is returned. It also assigns instance variables from the ``pybald.extension``
    environ variables that can be set from other parts of the WSGI pipeline.
    
    This decorator is completely *optional* but recommended for making working with requests
    and responses easier.
    '''
    def replacement(self, environ, start_response):
        req = Request(environ)

        # add any url variables as members of the controller
        for key in req.urlvars.keys():
            #Set the controller object to contain the url variables
            # parsed from the dispatcher / router
            setattr(self,key,req.urlvars[key])

        # this code defines the template id to match against
        # template path = controller name + '/' + action name (except in the case of)
        # index
        # if not hasattr(self, "template_id"):
        if method.__name__ not in ('index','__call__'):
            self.template_id = "{0}/{1}".format(camel_to_underscore(self.controller_pattern.search(self.__class__.__name__).group(1)), method.__name__)
        else:
            self.template_id = camel_to_underscore(self.controller_pattern.search(self.__class__.__name__).group(1))
        
        # add the pybald extension dict to the controller
        # object
        extension = req.environ.get('pybald.extension',None)
        if extension:
            for key in extension.keys():
                setattr(self,key,extension[key])

        # Return either the controllers _pre code, whatever 
        # is returned from the controller
        # or the view. So pre has precedence over 
        # the return which has precedence over the view
        resp = self._pre(req) or method(self,req) or self._view()

        # if the response is currently just a string
        # wrap it in a response object
        if isinstance(resp, basestring):
            resp = Response(body=resp)

        # run the controllers post code
        self._post(req,resp)

        return resp(environ, start_response)
    # restore the original function name
    replacement.__name__ = method.__name__
    return replacement


asset_tag_cache = {}
class Page(dict):
    def __init__(self, version=None):
        self['title'] = None
        self['metas'] = []
        self['headers'] = []
        self.version = media_version
        self['asset_tags'] = {}

    def compute_asset_tag(self, filename):
        asset_tag = asset_tag_cache.get(filename, None)
        if not asset_tag:
            asset_tag = str(int(round(os.path.getmtime(os.path.join(project_path,"content",filename.lstrip("/"))) )) ) 
            asset_tag_cache[filename] = asset_tag
        return asset_tag

    def add_js(self, filename):
        filename += '?v=%s' % (self.compute_asset_tag(filename))
        self['headers'].append('''<script type="text/javascript" src="%s"></script>''' % (str(filename)) )

    def add_css(self, filename, media="screen"):
        filename += '?v=%s' % (self.compute_asset_tag(filename))
        self['headers'].append('''<link type="text/css" href="%s" media="%s" rel="stylesheet" />''' % (str(filename),str(media)) )

class Safe(object):
    pass

class BaseController():
    '''Base controller that includes the view and a default index method.'''

    controller_pattern = re.compile(r'(\w+)Controller')

    def __init__(self):
        '''
        Initialize the base controller with a page object. 
        
        Page dictionary controls title, headers, etc...
        '''
        self.page = Page()
        self.error = None
        self.user = None
        self.session = None

        if page_options:
            for key in page_options.keys():
                setattr(self, key, page_options[key]) 
                
    @action
    def index(self,req):
        '''default index action'''
        pass
        
    def _pre(self, req):
        '''Code to run before any action.'''
        pass

    def _post(self, req, resp):
        '''Code to run after any action.'''
        # Closes the db Session object. Required to avoid holding sessions
        # indefinitely and overruning the sqlalchemy pool
        pass

    def _redirect_to(self, url, *pargs, **kargs):
        '''Redirect the controller'''
        return redirect_to(url,*pargs,**kargs)

    def _not_found(self, text=None):
        raise exc.HTTPNotFound(text)

    def _status(self, code):
        raise exc.status_map[int(code)]

    def _view(self,user_dict=None):
        '''Method to invoke the template engine and display a view'''
        view = engine
        # user supplied dictionary, otherwise create a dictionary
        # from the controller
        data = user_dict or self.__dict__ or {}
        if data['template_id'] is None:
            data['template_id'] = self.template_id

        view_data = view(data)

        # A very simple lock to avoid exposing the Model API
        # in the mako template. The "protect" method isn't very
        # secure, more of a protection against accidental invocation
        # of the get, delete, load, etc... methods in the template.
        
        # FIXME: This experiment failed, I believe the file access in the template engine
        # allows eventlet to thread switch in the middle, causing other objects to fail
        # because they don't have access to the model API. Still thinking.
        # try:
        #     print "LOCKING AND BLOCKING"
        #     models.Model.protect()
        #     for x in range(1000):
        #         i = 0
        #         while i < 50000:
        #             i+=1
        #     view_data = view(data)
        # finally:
        #     # regardless of the exception state, the
        #     # models must be unlocked
        #     print "UNLOCKING"
        #     models.Model.protect(False)
        return view_data
        
class BaseControllerTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()