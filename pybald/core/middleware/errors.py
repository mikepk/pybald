#!/usr/bin/env python
# encoding: utf-8

from webob import Response, exc
from pybald.core.templates import render as template_engine
import logging
console = logging.getLogger(__name__)


class ErrorMiddleware:
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
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()
        self.error_controller = error_controller

    def __call__(self, environ, start_response):
        #pass through if no exceptions occur
        try:
            # catch stupid URLs before getting into webob
            try:
                unicode(environ['PATH_INFO'])
            except UnicodeDecodeError:
                return Response(status=400, body="""<h1>Bad Request</h1>""")(environ, start_response)
            return self.application(environ, start_response)
        # handle HTTP errors
        except exc.HTTPException, err:
            # if the middleware is configured with an error controller
            # use that to display the errors
            console.debug("HTTP Exception thrown {0}".format(err))
            if self.error_controller:
                handler = self.error_controller(status_code=err.code)

                try:
                    # try executing error_handler code
                    # otherwise re-raise the exception
                    return handler(environ, start_response)
                except Exception:
                    console.exception("Exception thrown during error_controller handling")
                    raise
            else:
                # HTTPExceptions are also WSGI apps and can be called as such
                return err(environ, start_response)
        except Exception, err:
            console.exception("General Exception thrown")
            if self.error_controller:
                handler = self.error_controller(message=str(err))
            else:
                # create a generic HTTP server Error webob exception
                handler = exc.HTTPServerError('General Fault')
            return handler(environ, start_response)


def pybald_error_template():
    '''
    This method is a shim between the old view error template function and the
    new template rendering methods. It should not be used and is present only
    to maintain backward compatibility.

    This is targeted for deprecation.
    '''
    console.warn("pybald_error_template is deprecated in pybald 0.2.0")
    return template_engine._get_template('stack_trace')
