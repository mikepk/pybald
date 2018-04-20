#!/usr/bin/env python
# encoding: utf-8


class UserManager(object):
    '''Code to manage users, implemented as WSGI middleware. 

    This middleware will set REMOTE_USER as well as the pybald context object 
    within the WSGI environ. This allows any other WSGI or pybald aware code
    to inspect the environ for the current authenticated user.'''

    def __init__(self, application=None, user_class=None):
        self.user_class = user_class
        if application is None:
            raise ValueError("User Manager Middleware doesn't work stand alone, it is expected to wrap another application.")
        self.application = application

    def __call__(self, environ, start_response):
        session = environ.get('pybald.session', None)
        environ['REMOTE_USER'] = session.user

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

        # update or create the pybald.extension for other pybald aware WSGI code
        environ['pybald.extension'] = environ.get('pybald.extension', {})
        environ['pybald.extension']['user'] = environ['REMOTE_USER']
        # call the next part of the pipeline
        return self.application(environ, start_response)
