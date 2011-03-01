#!/usr/bin/env python
# encoding: utf-8
"""
Router.py

Created by mikepk on 2009-06-28.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os  #, glob
import unittest
import re

from webob import Request, Response, exc

from routes import Mapper, request_config, URLGenerator
# handle Mako's top level lookup
from mako import exceptions

import app.controllers
import project

from pybald.util import camel_to_underscore

class Router:
    '''router class for connecting controllers to URLs'''
    def __init__(self,application=None,routes=None):
        self.controllers = {}
        # default mapper was switched to explicit
        # explains all the mapper weirdness I was seeing
        # explicit turns off route memory and 'index' for
        # default action
        # initialize Router
        self.map = Mapper(explicit=False)
        if not routes:
            raise Exception("Route mapping required, please pass in a routing function to Router init.")
        routes(self.map)
        self.load()

    def load(self):
        '''Scans the controllers path and imports all controllers with a pybald name.'''

        controller_names = []
        for controller in app.controllers.__all__:
            #lowercase and strip 'Controller'
            controller_name = re.search('(\w+)Controller',controller).group(1)
            controller_name = camel_to_underscore(controller_name).lower()
            controller_names.append(controller_name)
            self.controllers[controller_name]={'name':controller,'module':getattr(app.controllers,controller)}
        
        # register the controller module names
        # with the mapper, creates the internal regular
        # expressions
        self.map.create_regs(controller_names)

    def deferred_exception(self, func, exc_info):
        '''Function wrapper / closure to re-raise exceptions that occur too early to be displayed.'''
        def raise_deferred(environ,start_response):
            raise exc_info[0], exc_info[1], exc_info[2]
        return raise_deferred


    def __call__(self,environ,start_response):
        '''WSGI app, Router is called directly to actually route the url to the target'''
        req = Request(environ)
        #method override
        # for REST architecture, this allows a POST parameter of _method
        # to be used to override POST with alternate HTTP verbs (PUT, DELETE)
        old_method = None
        req.errors = 'ignore'
        params = req.POST
        if '_method' in req.POST:
            old_method = environ['REQUEST_METHOD']
            environ['REQUEST_METHOD'] = req.POST['_method'].upper()
            if req.POST:
                del req.POST['_method']
            if project.debug:
                print "Changing request method to %s" % environ['REQUEST_METHOD']


        # routes config object, this must be done on every request.
        # sets the mapper and allows link_to and redirect_to to
        # function on routes
        config = request_config()
        config.mapper = self.map
        config.environ = environ

        match = config.mapper_dict
        route = config.route
        url = URLGenerator(self.map, environ)
        environ['wsgiorg.routing_args'] = ((url), match)
        environ['routes.route'] = route
        environ['routes.url'] = url


        # TODO: Setup the framework to use the URLGenerator instead of url_for
        # environ['pybald.extension']['__url'] = environ['routes.url']

        # Add pybald extension, normally gets assigned to controller object
        environ['pybald.extension'] = environ.get('pybald.extension', {})
        environ['pybald.extension']["url_for"] = url
        # environ['pybald.extension']["redirect_to"] = lambda url_text: Response(location=url(url_text),status=302)

        # defines the redirect method. In this case it generates a
        # Webob Response object with the location and status headers
        # set
        config.redirect = lambda url: Response(location=url,status=302)
        

        # debug print messages
        if project.debug:
            print '============= '+req.path+' =============='
            print 'Method: %s' % req.method

        # use routes to match the url to a path
        # urlvars will contain controller + other non query string
        # URL data. Middleware above this can override and set urlvars
        # and the router will use those values.
        # TODO: allow individual variable overrides?
        urlvars = environ.get('urlvars', self.map.match(req.path))
        # urlvars = self.map.match(req.path)
        if not urlvars: urlvars = {}
        
        # restore the original method if it was modified for REST purposes
        # when dealing with browser's limited GET/POST only verbs
        # if old_method:
        #     environ['REQUEST_METHOD'] = old_method


        req.urlvars = urlvars
        environ['urlvars'] = urlvars
        if urlvars:
            try:
                controller = urlvars["controller"]
                action = urlvars["action"]
                if project.debug:
                    for key in urlvars.keys():
                        print '''%s: %s''' % (key, urlvars[key])

                #methods starting with underscore can't be used as actions
                if re.match('^\_',action):
                    raise exc.HTTPNotFound("Invalid Action")
                    
                # create controller instance from controllers dictionary
                # using routes 'controller' returned from the match
                controller = getattr(self.controllers[controller]['module'], self.controllers[controller]['name'])()
                handler = getattr(controller, action)
                
            # only catch the KeyError/AttributeError for the controller/action search
            except (KeyError, AttributeError):
                raise exc.HTTPNotFound("Missing Controller or Action")

        # No URL vars means nothing matched in the mapper function
        else:
            raise exc.HTTPNotFound("No URL match")

        try:
            # call the action we determined from the mapper
            return handler(environ,start_response)
        # This is a mako 'missing template' exception
        except exceptions.TopLevelLookupException:
            raise exc.HTTPNotFound("Missing Template")        
        except:
            # All other program errors get re-raised
            # e.g. a 500 server error
            raise

                
class routerTests(unittest.TestCase):
    def setUp(self):
        pass

    def testMap(self):
        router = Router()

    def testRoute(self):
        pass

    def testLoad(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
