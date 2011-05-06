#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import re

from webob import Request, Response, exc

from routes import Mapper, request_config, URLGenerator
# handle Mako's top level lookup
from mako import exceptions

import project
debug = project.debug

# load the controllers from the project defined path
controllers = __import__(project.controllers_module, globals(), locals(), [project.controllers_module], 1)

from pybald.util import camel_to_underscore, underscore_to_camel

class Router(object):
    # class method match patterns
    has_underscore = re.compile(r'^\_')
    controller_pattern = re.compile(r'(\w+)_controller')
    
    def __init__(self, application=None, routes=None):
        '''
        Create a Router object, the core of the pybald framework.
        
        :param application:  WSGI application/middleware that is to be *wrapped* by the router 
                             in the web app pipeline.
        
        :param routes: An instance of a Routes mapper (for parsing and matching urls)
        
        '''
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
        '''
        Loads controllers from app.controllers. Uses the controller name to define a path
        to controller mapping. It does some text munging to camel-case the module name 
        to look up the expected classname in the modules. It loads all controller candidates into
        a mapping block to look up URLs against. 
        
        Called only once at the start of a pybald application.
        '''

        controller_names = []
        for controller in controllers.__all__:
            controller_path_name = self.controller_pattern.search(controller).group(1)
            controller_names.append(controller_path_name)
            # self.controllers holds paths to map to modules and controller names
            self.controllers[controller_path_name] = {'name':underscore_to_camel(controller),'module':getattr(controllers, controller)}
        
        # register the controller module names
        # with the mapper, creates the internal regular
        # expressions
        self.map.create_regs(controller_names)


    def __call__(self, environ, start_response):
        '''
        A Router instance is a WSGI app. It accepts the standard WSGI call signature of
        ``environ``, ``start_response``. 
        
        The Router has a few jobs. First it uses the Routes package to
        compare the requested path to available url patterns that have
        been loaded and passed to the Router upon init.
        
        Router is the most *framework-like* component of Pybald. In addition to
        dispatching urls to controllers, it also allows 'method override' 
        behavior allowing other HTTP methods to be invoked such as ``put`` and
        ``delete``.
        '''
        req = Request(environ)
        #method override
        #===============
        # for REST architecture, this allows a POST parameter of _method
        # to be used to override POST with alternate HTTP verbs (PUT, DELETE)
        req.errors = 'ignore'
        params = req.POST
        if '_method' in req.params:
            environ['REQUEST_METHOD'] = req.params['_method'].upper()
            try:
                del req.POST['_method']
            except:
                pass
            # Experiment, is it worth it to change get method too?
            try:
                del req.GET['_method']
            except:
                pass


            if debug:
                print "Changing request method to {0}".format(environ["REQUEST_METHOD"])


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

        # defines the redirect method. In this case it generates a
        # Webob Response object with the location and status headers
        # set
        config.redirect = lambda url: Response(location=url, status=302)        

        # debug print messages
        if debug:
            print ''.join(['============= ',req.path,' =============='])
            print 'Method: {0}'.format(req.method)

        # use routes to match the url to a path
        # urlvars will contain controller + other non query string
        # URL data. Middleware above this can override and set urlvars
        # and the router will use those values.
        # TODO: allow individual variable overrides?
        urlvars = environ.get('urlvars', self.map.match(environ=environ)) or {}

        # lifted from Routes middleware, handles 'redirect'
        # routes (map.redirect)
        if route and route.redirect:
            route_name = '_redirect_%s' % id(route)
            location = url(route_name, **match)
            return Response(location=location, status=route.redirect_status)(environ, start_response)


        req.urlvars = urlvars
        environ['urlvars'] = urlvars
        if urlvars:
            controller = urlvars["controller"]
            action = urlvars["action"]

            #methods starting with underscore can't be used as actions
            if self.has_underscore.match(action):
                raise exc.HTTPNotFound("Invalid Action")
                
            if debug:
                print "\n".join(['''{0}: {1}'''.format(key, value) for key, value in urlvars.items()])

            try:
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
