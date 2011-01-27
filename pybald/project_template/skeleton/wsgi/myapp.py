import sys
import os

# mod_wsgi restricts stdout, so switch it to stderr
sys.stdout = sys.stderr

# find out where this module lives, set the project path accordingly
project_path,script_path = os.path.split(os.path.dirname( os.path.realpath( __file__ ) ))

# add the project and pybald paths to the sitedir
# TODO: make pybald installable so this is unnecesary
import site
site.addsitedir(project_path)
import project
site.addsitedir(project.pybald_path)
site.addsitedir(project.get_toplevel())

from pybald.core.Router import Router
from pybald.core.SessionManager import SessionManager
from pybald.core.UserManager import UserManager
from pybald.core.ErrorMiddleware import ErrorMiddleware
from pybald.core.PybaldLogger import PybaldLogger

# load the error controller so that the ErrorMiddleware
# has somewhere to route the request if an error occurs
from app.controllers.ErrorController import ErrorController
    
# The main application pipeline
# Include all WSGI middleware here. The order of 
# web transaction will flow from the bottom of this list
# to the top, and then back out. The pybald Router
# should usually be the first item listed.
app = Router(routes=project.set_routes)
app = UserManager(app)
app = SessionManager(app)
app = ErrorMiddleware(app, error_controller=ErrorController)
#app = PybaldLogger(app,'/tmp/pybald.log', project_name=project.project_name, level="INFO")

from static_serve import static_serve
app = static_serve(app, path='content')


# mod_wsgi looks for 'application'
application = app

# called directly enable the interactive debugger
# requires 'paste' be installed
def main():
    '''A simple server startup if module is called directly'''
    from paste import httpserver
    # use this for the interactive debugger
    #from paste.evalexception import EvalException

    # add the static server component
    from static_serve import static_serve
    my_app = static_serve(app, path='content')

    httpserver.serve(my_app, host='0.0.0.0', port=8080)
    
#use when moduled called directly, runs without apache, spawning, or nginx
if __name__ == '__main__':
    main()
