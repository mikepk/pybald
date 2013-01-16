#!/usr/bin/env python
# encoding: utf-8
# """
# BaseController.py
#
# Base Controller that all Pybald controllers inherit from.
#
# Created by mikepk on 2009-06-29.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.
# """

import sys
import os
import unittest

import os.path

from functools import update_wrapper, wraps
from pybald.core.templates import engine as view_engine

from webob import Request, Response
from webob import exc
import re

from pybald.db.models import session
from pybald.util import camel_to_underscore

from routes import redirect_to
import project
media_version = project.media_version
project_path = project.path
page_options = project.page_options

from pybald.db import models

import json
import random

controller_pattern = re.compile(r'(\w+)Controller')


# action / method decorator
def action(method):
    '''
    Decorates methods that are WSGI apps to turn them into pybald-style actions.

    :param method: A method to turn into a pybald-style action.

    This decorator is usually used to take the method of a controller instance
    and add some syntactic sugar around it to allow the method to use WebOb
    Request and Response objects. It will work with any method that
    implements the WSGI spec.

    It allows actions to work with WebOb request / response objects and handles
    default behaviors, such as displaying the view when nothing is returned,
    or setting up a plain text Response if a string is returned. It also
    assigns instance variables from the ``pybald.extension`` environ variables
    that can be set from other parts of the WSGI pipeline.

    This decorator is optional but recommended for making working
    with requests and responses easier.
    '''
    template_name = method.__name__
    if template_name in ('index','__call__'):
        template_name = ''

    @wraps(method)
    def action_wrapper(self, environ, start_response):
        req = Request(environ)
        # add any url variables as members of the controller
        for key in req.urlvars.keys():
            #Set the controller object to contain the url variables
            # parsed from the dispatcher / router
            setattr(self, key, req.urlvars[key])

        # this code defines the template id to match against
        # template path = controller name + '/' + action name (except in the case of)
        # index
        try:
            template_root_name = camel_to_underscore(
                      controller_pattern.search(self.__class__.__name__
                                           ).group(1))
        except AttributeError:
            template_root_name = ''
        self.template_id = "/".join(filter(lambda x: x != '', [template_root_name, template_name]))

        # add the pybald extension dict to the controller
        # object
        for key, value in req.environ.get('pybald.extension', {}).items():
            setattr(self, key, value)
        setattr(self, 'request', req)
        setattr(self, 'request_url', req.url)

        # Return either the controllers _pre code, whatever
        # is returned from the controller
        # or the view. So pre has precedence over
        # the return which has precedence over the view
        none_func = lambda *pargs, **kargs: None
        pre = getattr(self, '_pre', none_func)
        post = getattr(self, '_post', none_func)
        view = getattr(self, '_view', none_func)

        resp = pre(req) or method(self, req) or view()

        # if the response is currently a string
        # wrap it in a response object
        if isinstance(resp, basestring):
            resp = Response(body=resp, charset="utf-8")
        # run the controllers post code
        post(req, resp)
        return resp(environ, start_response)
    return action_wrapper

import hashlib
import base64

def caching_pre(keys, method_name, prefix=''):
    '''Decorator for pybald _pre to return cached responses if available.'''
    if keys is None:
        keys = []

    def pre_wrapper(pre):
        def replacement(self, req):
            val = ":".join([prefix] + [str(getattr(self, k, '')) for
                        k in keys] + [method_name])
            self.cache_key = base64.urlsafe_b64encode(hashlib.md5(val).digest())
            resp = project.mc.get(self.cache_key)
            if resp:
                return resp
            return pre(req)
        return replacement
    return pre_wrapper

def caching_post(time=0):
    '''Decorator for pybald _post to cache/store responses.'''
    def post_wrapper(post):
        def replacement(self, req, resp):
            post(req, resp)
            if 'X-Cache' not in resp.headers:
                resp.headerlist.append(('X-Cache', 'MISS'))
                project.mc.set(self.cache_key, resp, time)
            else:
                resp.headers['X-Cache']='HIT'
        return replacement
    return post_wrapper


# memcache for actions
def action_cached(prefix=hex(random.randrange(0, 2 ** 32 - 1)), keys=None, time=0):
    '''
    The default prefix is reset whenever the code is reloaded.

    This provides a nice way to cache static content for the duration of the
    application lifespan.
    '''
    if keys is None:
        keys = []
    def cached_wrapper(my_action_method):
        @wraps(my_action_method)
        def replacement(self, environ, start_response):
            # bind newly wrapped methods to self
            self._pre = caching_pre(keys, my_action_method.__name__, prefix=prefix)(self._pre).__get__(self, self.__class__)
            self._post = caching_post(time)(self._post).__get__(self, self.__class__)
            return my_action_method(self, environ, start_response)
        return replacement
    return cached_wrapper


asset_tag_cache = {}
class Page(dict):
    def __init__(self, version=None):
        self['title'] = None
        self['metas'] = []
        self['headers'] = []
        self.version = media_version
        self['asset_tags'] = {}

        #self.sm = project.registry.sm

    def _compute_asset_tag(self, filename):
         asset_tag = asset_tag_cache.get(filename, None)
         try:
             if not asset_tag:
                 asset_tag = str(int(round(os.path.getmtime(os.path.join(project_path,"public",filename.lstrip("/"))) )) )
                 asset_tag_cache[filename] = asset_tag
         except OSError:
            asset_tag_cache[filename] = "xxx"
         return "?v={0}".format(asset_tag)

    def add_js(self, filename):
        return '''<script type="text/javascript" src="{0}{1}"></script>'''.format(filename, self._compute_asset_tag(filename) )

    def add_css(self, filename, media="screen"):
        return '''<link type="text/css" href="{0}{2}" media="{1}" rel="stylesheet" />'''.format(filename, str(media), self._compute_asset_tag(filename) )



class Safe(object):
    pass

class BaseController(object):
    '''Base controller that includes the view and a default index method.'''

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


    def __before__(self, req):
        '''Code to run before any action.'''
        return self._pre(req)

    def __after__(self, req, resp):
        '''Code to run after any action.'''
        return self._post(req, resp)


    def _pre(self, req):
        '''Code to run before any action.'''
        pass

    def _post(self, req, resp):
        '''Code to run after any action.'''
        pass

    def _redirect_to(self, *pargs, **kargs):
        '''Redirect the controller'''
        return redirect_to(*pargs,**kargs)

    def _not_found(self, text=None):
        raise exc.HTTPNotFound(text)

    def _status(self, code):
        raise exc.status_map[int(code)]

    def _view(self, user_dict=None, helpers=None):
        '''Method to invoke the template engine and display a view'''
        # view = engine
        # user supplied dictionary, otherwise create a dictionary
        # from the controller
        data = user_dict or self.__dict__ or {}
        # prob should check for keyerror
        data['template_id'] = data.get('template_id', getattr(self, "template_id", None))
        # ] is None:
        #     data['template_id'] = self.template_id
        # if helpers:
        #     data.update(helpers)
        return view_engine(data)

    def _JSON(self, data, status=200):
        '''Return JSON object with the proper-ish headers.'''
        res = Response( body=json.dumps(data),
            status=status,
            # wonky Cache-Control headers to stop IE6 from caching content
            cache_control="max-age=0,no-cache,no-store,post-check=0,pre-check=0",
            expires = "Mon, 26 Jul 1997 05:00:00 GMT",
            content_type = "application/json",
            charset = 'UTF-8'
            )
        return res

class BaseControllerTests(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()