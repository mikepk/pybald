#!/usr/bin/env python
# encoding: utf-8
"""
ErrorMiddleware.py

Created by mikepk on 2010-04-14.
Copyright (c) 2010 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import datetime

from webob import Request, Response, exc
from mako import exceptions

class ErrorMiddleware:
    '''Code to handle errors, implemented as WSGI middleware.'''
    def __init__(self,application=None,error_controller=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()
        self.error_controller = error_controller

    def __call__(self,environ,start_response):
        req = Request(environ)
        #pass through if no exceptions occur
        try:
            return req.get_response(self.application)(environ,start_response)
        # handle HTTP errors
        except exc.HTTPException, err:
            if self.error_controller:
                try:
                    controller = self.error_controller()
                    action = self.error_controller.error_map[err.code]
                    handler = getattr(controller,action)
                    #return handler(environ,start_response)
                except (KeyError, AttributeError):
                    controller = self.error_controller()
                    handler = controller
                except Exception, ex:
                    handler = err
                    #return err(environ,start_response)
                
                try:
                    return handler(environ,start_response)
                except Exception:
                    raise
            else:
                return err(environ,start_response)
                
        except Exception, err:
            if self.error_controller:
                controller = self.error_controller()
                handler = controller
                controller.message=str(err)
                return handler(environ,start_response)
            else:
                # create a generic HTTP server Error webob exception
                return exc.HTTPServerError()(environ,start_response)
        # finally:
        #     sys.stderr.write(str(err))

class ErrorMiddlewareTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()