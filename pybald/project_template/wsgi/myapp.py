#!/usr/bin/env python
# encoding: utf-8
import sys
import os

# mod_wsgi restricts stdout, so switch it to stderr
sys.stdout = sys.stderr

# find out where this module lives, set the project path accordingly
project_path, script_path = os.path.split(
                                os.path.dirname(os.path.realpath(__file__)))

# add the project and pybald paths to the sitedir
# TODO: make pybald installable so this is unnecesary
import site
site.addsitedir(project_path)
import project
site.addsitedir(project.toplevel)


if __name__ == '__main__' and __package__ is None:
    __import__(project.package_name, globals(), locals(),
                        ['wsgi'], -1)
    __package__ = project.package_name+'.wsgi'

from pybald.core.router import Router
from pybald.core.errors import ErrorMiddleware
# from pybald.core.sessions import SessionManager
# from pybald.core.users import UserManager
# from pybald.core.pybald_logger import PybaldLogger
# from pybald.core.db_middleware import DbMiddleware

# load the application
# loading models and controllers here initializes them
from ..app import urls, models, controllers

# load the error controller so that the ErrorMiddleware
# has somewhere to route the request if an error occurs
from ..app.controllers import ErrorController
# from quiz_site.app.models.session import Session
# from quiz_site.app.models.user import User

# The main application pipeline
# Include all WSGI middleware here. The order of
# web transaction will flow from the bottom of this list
# to the top, and then back out. The pybald Router
# should usually be the first item listed.
# ----------------------------------
app = Router(controllers=controllers, routes=urls.map)
# app = UserManager(app, user_class=User)
# app = SessionManager(app, session_class=Session)
# app = DbMiddleware(app)
app = ErrorMiddleware(app, error_controller=ErrorController)
# ----------------------------------
#    ↑↑↑                  ↓↓↓
#    ↑↑↑                  ↓↓↓
#   Request              Response


# apache / mod_wsgi looks for 'application'
application = app


# called directly runs a simple dev server
# using the wsgiref server
def main():
    '''A simple server startup if module is called directly'''
    from optparse import OptionParser
    from wsgiref.simple_server import make_server
    from pybald.core.static_serve import StaticServer

    parser = OptionParser()
    parser.add_option("--host", default="0.0.0.0",
                      dest="host",
                      help="host ip to run")
    parser.add_option("-p", "--port",
                      type="int",
                      dest="port", default=8080,
                      help="the port to run on.")
    (options, args) = parser.parse_args()

    # add the static server component
    my_app = StaticServer(app, path='public')
    httpd = make_server(options.host, options.port, my_app)
    print("Serving on {0}:{1}...".format(options.host, options.port))
    httpd.serve_forever()
    sys.exit(1)


#use when moduled called directly, runs internal webserver
if __name__ == '__main__':
    main()
