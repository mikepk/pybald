#!/usr/bin/env python
# encoding: utf-8
"""
myapp.wsgi

Created by mikepk on 2009-06-28.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os

project_path = ''

import re

# where is this module, set the project path accordingly
project_path,script_path = os.path.split(os.path.dirname( os.path.realpath( __file__ ) ))

# Change this path for each site/install
# TODO: pybald core should probably be installed to be avail to all
# of python.
pybald_path = '/usr/share/enerd/'

import site
site.addsitedir(project_path)
site.addsitedir(pybald_path)

import project
from pybald.core.Router import Router

# create and load the url router
url_route = Router()
project.set_routes(url_route.map)
url_route.load()

def run_pipeline(environ,start_response):
    '''Sets up and executes the pipeline. Returns the execution of the response object.'''
    # setup the WSGI pipeline

    # run the first part of the pipeline, retrieves the
    # webob response object
    resp = url_route(environ,start_response)

    # Execute the response object which is a WSGI app
    # means it's called with environ and start_response
    return resp(environ,start_response)

# mod_wsgi calls 'application'
application = run_pipeline

# called directly enable the interactive debugger
# requires 'paste' be installed
def main():
    '''A simple server startup if module is called directly'''
    from paste.evalexception import EvalException
    from wsgiref.simple_server import make_server

    # a stupid static file server to serve data in 'content'
    # chained to the wsgi application so that 404's fall through to the app
    from static_serve import static_serve
    ss = static_serve(run_pipeline, 'content')
    
    make_server('', 8000, EvalException(ss.serve)).serve_forever()

#use when moduled called directly, runs without apache
if __name__ == '__main__':
    main()
