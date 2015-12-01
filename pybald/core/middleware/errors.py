#!/usr/bin/env python
# encoding: utf-8

from webob import Response, exc
# from six.moves.urllib.parse import unquote
import logging
log = logging.getLogger(__name__)

def create_default_error_controller():
    from pybald.core.controllers import Controller, action
    from pybald.context import render, config
    class DefaultErrorController(Controller):
        '''Minimum helpful error controller'''
        def __init__(self, status_code=500, message=None, exception=None):
            self.status_code = status_code
            self.message = message
            self.exception = exception

        @action
        def __call__(self, req):
            '''
            The ErrorController will return a formatted stack trace if in debug
            mode, or point to a regular error page otherwise.
            '''
            if 400 <= int(self.status_code) < 500:
                return req.get_response(self.exception)
            else:
                if config.debug:
                    stack_trace = render(template='stack_trace', data={'req': req})
                    return Response(body=stack_trace, status=self.status_code)
                else:
                    return req.get_response(exc.HTTPServerError('General Fault'))
    return DefaultErrorController

class ErrorMiddleware(object):
    '''
    Handles exceptions during web transactions.

    Implemented as WSGI middleware, this middleware wraps the application and
    intercepts errors and exceptions. The middleware makes a distinction between
    webob HTTP exceptions and other exception types.


    :param application:  WSGI application/middleware that is to be
                         *wrapped* by the error handler in the web app pipeline.

    :param error_controller:  A class that is used by the middleware to handle
                          errors for the project. When configured, an error_controller
                          instance is created and the WSGI response is passed to
                          the error_controller to handle.
    '''
    def __init__(self, application=None, error_controller=None):
        if error_controller is None:
            self.error_controller = create_default_error_controller()
        else:
            self.error_controller = error_controller

        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()

    def __call__(self, environ, start_response):
        #pass through if no exceptions occur
        try:
            return self.application(environ, start_response)
        # handle HTTP errors
        except exc.HTTPException as err:
            # if the middleware is configured with an error controller
            # use that to display the errors
            log.debug("HTTP Exception Thrown {0}".format(err.__class__))
            if self.error_controller:
                handler = self.error_controller(status_code=err.code, exception=err)

                try:
                    # try executing error_handler code
                    # otherwise re-raise the exception
                    return handler(environ, start_response)
                except Exception:
                    log.exception("Exception thrown during error_controller handling")
                    raise
            else:
                # HTTPExceptions are also WSGI apps and can be called as such
                return err(environ, start_response)
        except Exception as err:
            log.exception("General Exception thrown")
            if self.error_controller:
                handler = self.error_controller(message=str(err), exception=err)
            else:
                # create a generic HTTP server Error webob exception
                handler = exc.HTTPServerError('General Fault')
            return handler(environ, start_response)
