#!/usr/bin/env python
# encoding: utf-8

from webob import Request,Response

# from app.models import User
import project
#total hack to get the User class with the proper namespace
User = getattr(__import__(project.models_module, globals(), locals(), ["User"], 1), "User")

class UserManager(object):
    '''Code to handle anonymous and user sessions, implemented as WSGI middleware.'''

    def __init__(self,application=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self,environ,start_response):
        req = Request(environ)

        session = environ.get('pybald.session', None)
        if session and session.user_id:
                if session.user:
                    environ['REMOTE_USER'] = session.user
                else:
                    try:
                        environ['REMOTE_USER'] = User.get(id=session.user_id)
                    except User.NotFound:
                        environ['REMOTE_USER'] = None
        else:
            environ['REMOTE_USER'] = None

        if environ['REMOTE_USER']:
            # Continuously validate user sessions
            # TODO: Clean up our app-level login code a lot...

            # Look for a "valid" method on User
            try:
                valid = getattr(environ['REMOTE_USER'], "valid")
            except AttributeError:
                # (If this method isn't defined, do nothing.)
                pass
            else:
                # If available, call it, and expect a Boolean:
                # If False, end the session right now.
                if not valid():
                    environ['REMOTE_USER'] = None
                # Otherwise, do nothing

        # update or create the pybald.extension to populate controller instances
        environ['pybald.extension'] = environ.get('pybald.extension', {})
        environ['pybald.extension']['user'] = environ['REMOTE_USER']

        # call the next part of the pipeline
        resp = req.get_response(self.application)
        return resp(environ,start_response)
