#!/usr/bin/env python
# encoding: utf-8
"""
router.py

Created by mikepk on 2009-06-28.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os, glob
import unittest
import re

from webob import Request, Response
from webob import exc

from routes import Mapper, request_config, url_for
from mako import exceptions

import pybald.core
import app.controllers

import logging
LOG_FILENAME = '/tmp/logging_example.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

# extract the package path for controllers
controller_path = app.controllers.__path__[0]

class Router:
    '''router class for connecting controllers to URLs'''
    def __init__(self):
        self.controllers = {}
        self.map = Mapper()

    def load(self):
        '''Scans the controllers path and imports all controllers with a canonical pybald name.'''
        controller_names = []
        for modulefile in glob.iglob( os.path.join(controller_path,"*Controller.py") ):
            modname = re.search('(\w+Controller)\.py',modulefile).group(1)
            imp_modname = 'app.controllers.'+modname
            controller_name = re.search('(\w+)Controller',modname).group(1).lower()
            controller_names.append(controller_name)
            try:
                module = __import__(imp_modname, globals(), locals(), [modname], -1)
            except (ImportError, SyntaxError),e:
                module = __import__('app.controllers.ErrorController', globals(), locals(), ['ErrorController'], -1)

                raise
            # add the module name to the list of urls
            self.controllers[controller_name]={'name':modname,'module':module}
        # register the controller module names
        # with the mapper, creates the internal regular
        # expressions
        self.map.create_regs(controller_names)
        
    def __call__(self,environ,start_response):
        '''WSGI app, Router is called directly to actually route the url to the target'''
        req = Request(environ)

        # TODO: remove the debug content before publishing
        # debug, does this work?
        sys.stdout = environ['wsgi.errors']

        # routes config object, this must be done on every request.
        # sets the mapper and allows link_to and redirect_to to
        # function on routes
        config = request_config()
        config.mapper = self.map
        config.environ = environ
        config.redirect = lambda url: Response(location=url,status=302)
        
        # debug print messages
        # TODO: remove these debug messages before publishing this
        print '============= '+req.path+' =============='
        # use routes to match the url to a path
        # urlvars will contain controller + other non query
        # URL data
        urlvars = self.map.match(req.path)
        if not urlvars: urlvars = {}
        req.urlvars = urlvars
        environ['urlvars'] = urlvars
        if urlvars:
            try:
                controller = urlvars["controller"]
                action = urlvars["action"]
                for key in urlvars.keys():
                    print '''%s: %s''' % (key, urlvars[key])
                # print 'Controller: '+controller+' Action: '+action
                #methods starting with underspybald.core can't be used as actions
                if re.match('^\_',action):
                    return exc.HTTPNotFound('invalid action')
                #(environ, start_response)
                # create controller instance from controllers dictionary
                # using routes 'controller' returned from the match
                controller = getattr(self.controllers[controller]['module'], self.controllers[controller]['name'])()
                handler = getattr(controller,action)
                
            # only catch the KeyError/AttributeError for the controller/action search
            except (KeyError, AttributeError):
                # 404 error
                controller = getattr(self.controllers['error']['module'], self.controllers['error']['name'])()
                handler = getattr(controller,'not_found')

        # No URL vars means nothing matched in the mapper function
        else:
            controller = getattr(self.controllers['error']['module'], self.controllers['error']['name'])()
            handler = getattr(controller,'not_found')


        try:
            # call the action we determined from the mapper
            # alm = ActionLogManager(handler).process_log
            # resp = handler(environ,start_response)
            return handler(environ,start_response)
            #resp(environ,start_response)
            # SessionManager(alm).process_session(environ,start_response)
            # resp = SessionManager(handler).process_session(environ,start_response)
            # return resp(environ,start_response)
        # This is a mako 'missing template' exception
        except exceptions.TopLevelLookupException:
            controller = getattr(self.controllers['error']['module'], self.controllers['error']['name'])()
            handler = getattr(controller,'not_found')
            # resp = SessionManager(handler).process_session(environ,start_response)
            # resp = handler(environ,start_response)
            # resp(environ,start_response)        
            return handler(environ,start_response)
            
        except:
            # # other program error
            # # 500
            # controller = getattr(self.controllers['error']['module'], self.controllers['error']['name'])()
            # handler = getattr(controller,'index')
            # return handler(environ,start_response)(environ,start_response)
            # # return SessionManager(handler).process_session(environ,start_response)(environ,start_response)

            # Debug version, this is the nice mako stack display in html format
            # This should be turned off for production
            # resp = Response(body=exceptions.html_error_template().render())
            # return resp(environ, start_response)
            return Response(body=exceptions.html_error_template().render())

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