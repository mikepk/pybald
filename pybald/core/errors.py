#!/usr/bin/env python
# encoding: utf-8

from webob import Request, Response, exc
from pybald.core.templates import engine as template_engine
import logging
console = logging.getLogger(__name__)

class ErrorMiddleware:
    '''
    Handles web exceptions

    Implemented as WSGI middleware.
    '''
    def __init__(self, application=None, error_controller=None):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()
        self.error_controller = error_controller

    def __call__(self, environ, start_response):
        req = Request(environ)
        #pass through if no exceptions occur
        try:
            return req.get_response(self.application)(environ, start_response)
        # handle HTTP errors
        except exc.HTTPException, err:
            # if the middleware is configured with an error controller
            # use that to display the errors
            console.debug("HTTP Exception thrown {0}".format(err))
            if self.error_controller:
                try:
                    handler = self.error_controller(status_code=err.code)
                    # controller.status_code = err.code
                    # action = self.error_controller.error_map[err.code]
                    # handler = controller #getattr(controller, action, None) or err
                except (KeyError, AttributeError):
                    handler = err
                except Exception:
                    handler = err
                try:
                    # try executing error_handler code
                    # otherwise re-raise the exception
                    return handler(environ, start_response)
                except Exception:
                    raise
            else:
                return err(environ, start_response)
        except Exception, err:
            console.exception("General Exception thrown")
            if self.error_controller:
                controller = self.error_controller()
                handler = controller
                controller.message = str(err)
                return handler(environ, start_response)
            else:
                # create a generic HTTP server Error webob exception
                return exc.HTTPServerError()(environ, start_response)


def send_error_email(host=None, html=None, text=None):
    if host:
        host = ': {0}'.format(host)
    else:
        host = ''

    me = "sysadmin@XXXX"
    you = "ops@XXXX"
    password = "XXXX"

    msg = MIMEMultipart('alternative')
    if text:
        msg.attach(MIMEText(text, 'text'))

    if html:
        msg.attach(MIMEText(html, 'html'))

    msg['Subject'] = '''{project_name} Exception'''.format(
                                    project_name=project.project_name.title())
    msg['From'] = "System Error{0} <{1}>".format(host, me)
    msg['To'] = you

    AuthUser=me
    AuthPass=password

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.ehlo()
    gmail.login(AuthUser, AuthPass)

    gmail.sendmail(me, [you], msg.as_string())
    gmail.close()

    return True


def pybald_error_template():
    '''
    This method is a shim between the old view error template function and the
    new template rendering methods. It should not be used and is present only
    to maintain backward compatibility.

    This is targeted for deprecation.
    '''
    return template_engine._get_template('stack_trace')
