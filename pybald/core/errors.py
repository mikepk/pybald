#!/usr/bin/env python
# encoding: utf-8

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
    return mako.template.Template(r"""\
<%!
    from mako.exceptions import RichTraceback
%>\
<%page args="full=True, css=True, error=None, traceback=None, req=None"/>\
% if full:
<html>
<head>
    <title>Pybald Runtime Error</title>
% endif
% if css:
    <meta name="viewport" content="480px" />
    <style>
        body { 
           font-family:Helvetica,Arial,verdana,sans-serif; 
           font-size: 1.2em; 
           margin:0; padding: 0;
           background-color: #FFE;
           }
        @media only screen and (max-device-width: 480px) {
                body {
                    width: 550px;
                }
            }
        ul { margin: 0; padding: 0; list-style: none; }
        #main { background-color: #FFB; border-bottom: 2px solid #CC9; }
        #urlvars { background-color: #FFF; border-bottom: 2px solid #EEE; }
        h3 { margin: 0; padding: 0; }
        .section { padding: 10px 20px 5px; }
        .stacktrace { margin:5px 5px 5px 5px; }
        .highlight { padding:0px 10px 0px 10px; background-color:gold; font-weight: bold; }
        .nonhighlight { padding:0px; background-color:#EFEFEF; }
        .sample { padding:10px; margin:10px 10px 10px 10px; font-family:monospace; }
        .sampleline { padding:0px 10px 0px 10px; }
        .sourceline { margin:5px 5px 10px 5px; font-family:monospace;}
        .location { font-size:80%; }
        .key { font-weight: bold; word-wrap:break-word; display: inline-block; text-align: right; width: 10em; }
        .value {  width: 70%; word-wrap:break-word; }
        #environment { font-size: 0.65em; background: #CCC; border-bottom: 1px dotted #EEE }
        #environment span { font-size: 0.65em; word-wrap:break-word; }
        #exception { color: #555555; font-size: 1.5em; letter-spacing: -1px; margin-bottom: 0.1em; }
        #environment table { table-layout: fixed; border-collapse: collapse; width: 100%; }
        #environment table td { vertical-align: top; border: 1px solid #DDD; }
        .env_key { font-weight: bold; }
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
<div class="section" id="main">
<h3 id="exception">${tback.errorname}: ${tback.message[:1024]}</h3>
% if req:
<ul>
<li><span class="key">request url:</span> <span class="sourceline">${req.url|h}</span></li>
<li><span class="key">request method:</span> <span class="sourceline">${req.environ.get("REQUEST_METHOD")|h}</span></li>
<li><span class="key">user:</span> <span class="sourceline">\
%try:
${req.remote_user.email|h}\
%except:
None\
%endtry
</span></li>
</ul>
</div>
<div class="section" id="urlvars">
<ul>
% for label, val in req.environ.get("urlvars",{}).items():
<li><span class="key">${label|h}:</span><span class="sourceline">${val|h}</span></li>
% endfor
</ul>
</div>
% endif
<div class="section" id="stacktrace">
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
</div>
%if req:
<div class="section" id="environment">
<h3>Environment</h3>
<table>
<tbody>
%for key in sorted(req.environ.keys()):
<tr><td>
<span class="env_key">
%try:
${key|h}\
%except Exception, err:
---${err}---\
%endtry
</span></td>
<td><span class="env_value">\
%try:
${str(req.environ[key])|h}
%except Exception, err:
---${err}---\
%endtry
</span></td>
</tr>
%endfor
</tbody>
</table>
</div>
%if full:
</body>
</html>
%endif
%endif
""", output_encoding=sys.getdefaultencoding(), encoding_errors='htmlentityreplace')


def send_error_email(host=None, html=None, text=None):
    if host:
        host = ': {0}'.format(host)
    else:
        host = ''

    me = "sysadmin@smarterer.com"
    you = "ops@smarterer.com"
    password = "thej7oyct5yoarg5"

    msg = MIMEMultipart('alternative')
    if text:
        msg.attach(MIMEText(text, 'text'))

    if html:
        msg.attach(MIMEText(html, 'html'))

    msg['Subject'] = '''Smarterer Exception'''.format(host)
    msg['From'] = "System Error{0} <{1}>".format(host, me)
    msg['To'] = you

    AuthUser=me #"sysadmin@smarterer.com"
    AuthPass=password #"thej7oyct5yoarg5"

    gmail = smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.ehlo()
    gmail.login(AuthUser, AuthPass)

    gmail.sendmail(me, [you], msg.as_string())
    gmail.close()

    return True

