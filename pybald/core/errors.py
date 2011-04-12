import sys
import os
import mako.template

import unittest

import datetime

from webob import Request, Response, exc
from mako import exceptions

class ErrorMiddleware:
    '''
    Handles web exceptions
    
    Implemented as WSGI middleware.
    '''
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
            # if the middleware is configured with an error controller
            # use that to display the errors
            if self.error_controller:
                try:
                    controller = self.error_controller()
                    controller.status_code = err.code
                    action = self.error_controller.error_map[err.code]
                    handler = getattr(controller, action, None) or err
                except (KeyError,AttributeError), ex:
                    handler = err
                except Exception, ex:
                    handler = err
                try:
                    # try executing error_handler code
                    # otherwise re-raise the exception
                    return handler(environ,start_response)
                except Exception:
                    raise
            else:
                return err(environ,start_response)
        # Not a web exception. Use the general error display.
        except Exception, err:
            if self.error_controller:
                controller = self.error_controller()
                handler = controller
                controller.message=str(err)
                return handler(environ,start_response)
            else:
                # create a generic HTTP server Error webob exception
                return exc.HTTPServerError()(environ,start_response)

def pybald_error_template():
    '''Lifts the Mako Exception Error template and adds an environment dump.'''
    return mako.template.Template(r"""
<%!
    from mako.exceptions import RichTraceback
%>
<%page args="full=True, css=True, error=None, traceback=None, req=None"/>
% if full:
<html>
<head>
    <title>Pybald Runtime Error</title>
% endif
% if css:
    <style>
        body { font-family:verdana; margin:10px 30px 10px 30px;}
        .stacktrace { margin:5px 5px 5px 5px; }
        .highlight { padding:0px 10px 0px 10px; background-color:#9F9FDF; }
        .nonhighlight { padding:0px; background-color:#DFDFDF; }
        .sample { padding:10px; margin:10px 10px 10px 10px; font-family:monospace; }
        .sampleline { padding:0px 10px 0px 10px; }
        .sourceline { margin:5px 5px 10px 5px; font-family:monospace;}
        .location { font-size:80%; }
        .env_key { display: inline-block; text-algin: right; width: 300px }
        .environment div { border-bottom: 1px dotted #EEE }
    </style>
% endif
% if full:
</head>
<body>
% endif

<h2>Error !</h2>
<%
    tback = RichTraceback(error=error, traceback=traceback)
    src = tback.source
    line = tback.lineno
    if src:
        lines = src.split('\n')
    else:
        lines = None
%>
<h3>${tback.errorname}: ${tback.message}</h3>

% if lines:
    <div class="sample">
    <div class="nonhighlight">
% for index in range(max(0, line-4),min(len(lines), line+5)):
    % if index + 1 == line:
<div class="highlight">${index + 1} ${lines[index] | h}</div>
    % else:
<div class="sampleline">${index + 1} ${lines[index] | h}</div>
    % endif
% endfor
    </div>
    </div>
% endif

<div class="stacktrace">
% for (filename, lineno, function, line) in tback.reverse_traceback:
    <div class="location">${filename}, line ${lineno}:</div>
    <div class="sourceline">${line | h}</div>
% endfor
</div>
%if req:
<h3>Environment</h3>
<div class="environment">
%for key in sorted(req.environ.keys()):
<div><span class="env_key">${key|h}</span><span class="env_value">${str(req.environ[key])|h}</span></div>
%endfor
</div>
%if full:
</body>
</html>
%endif
%endif
""", output_encoding=sys.getdefaultencoding(), encoding_errors='htmlentityreplace')
