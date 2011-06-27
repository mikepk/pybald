#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import mako.template

import unittest

import datetime

from webob import Request, Response, exc
from mako import exceptions
from sqlalchemy.exc import SQLAlchemyError

class SAException(SQLAlchemyError):
    def __init__(self, *pargs, **kargs):
        if kargs.get('error_controller'):
            self.error_controller = kargs.get('error_controller')
            del kargs["error_controller"]
        else:
            self.error_controller = None
        super(SAException, self).__init__(*pargs, **kargs)

    def __call__(self, environ, start_response):
        if self.error_controller:
            return self.error_controller(environ, start_response)

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
        # special case, when there's a SQLAlchemyError
        except SQLAlchemyError, err:
            # run the error controller and the re-raise an exception
            # passing the response up the chain (so we don't lose)
            # the original stack trace)
            controller = self.error_controller()
            handler = controller
            controller.message=str(err)
            resp = req.get_response(handler)
            raise SAException(error_controller=resp)
        # Not a web or SA exception. Use the general error display.
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
        body { 
           font-family:Helvetica,Arial,verdana,sans-serif; 
           font-size: 1.2em; 
           margin:10px 30px 10px 30px;
           background-color: #FFE;
           }
        .stacktrace { margin:5px 5px 5px 5px; }
        .highlight { padding:0px 10px 0px 10px; background-color:gold; font-weight: bold; }
        .nonhighlight { padding:0px; background-color:#EFEFEF; }
        .sample { padding:10px; margin:10px 10px 10px 10px; font-family:monospace; }
        .sampleline { padding:0px 10px 0px 10px; }
        .sourceline { margin:5px 5px 10px 5px; font-family:monospace;}
        .location { font-size:80%; }
        .env_key { display: inline-block; text-algin: right; width: 300px }
        .environment div { border-bottom: 1px dotted #EEE }
        #exception { }
        table { border-collapse: collapse; }
        table td { vertical-align: top; border: 1px solid #DDD; }
    </style>
% endif
% if full:
</head>
<body>
% endif

<%
    tback = RichTraceback(error=error, traceback=traceback)
    src = tback.source
    line = tback.lineno
    if src:
        lines = src.split('\n')
    else:
        lines = None
%>
<h3 id="exception">${tback.errorname}: ${tback.message}</h3>
% if req:
<div>method: <span class="sourceline">${req.environ.get("REQUEST_METHOD")|h}</span></div>
<div>url: <span class="sourceline">${req.environ.get("PATH_INFO")|h}</span></div>
% for label, val in req.environ.get("urlvars").items():
<div>${label|h}: <span class="sourceline">${val|h}</span></div>
% endfor
% endif
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
<table>
<tbody>
%for key in sorted(req.environ.keys()):
<tr><td>
<span class="env_key">${key|h}</span></td>
<td><span class="env_value">${str(req.environ[key])|h}</span></td>
</tr>
%endfor
</tbody>
</table>
</div>

% if req.environ.get('pybald.extension') and req.environ.get('pybald.extension').get('dbg_log'):
<h3>Debug Log</h3>
<div class="debug">
<pre>${req.environ['pybald.extension']['dbg_log'] | h}</pre>
</div>
%endif
%if full:
</body>
</html>
%endif
%endif
""", output_encoding=sys.getdefaultencoding(), encoding_errors='htmlentityreplace')
