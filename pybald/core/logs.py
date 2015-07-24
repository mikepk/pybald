#!/usr/bin/env python
# encoding: utf-8

#import sys
import unittest
#from webob import Request, Response

import logging
import logging.handlers
from textwrap import TextWrapper
log = logging.getLogger(__name__)


class WrappedFormatter(logging.Formatter):
    '''
    Formatter subclass that indents the messages by 20 characters and
    prepends sql> prompt.
    '''
    def __init__(self, *pargs, **kargs):
        logging.Formatter.__init__(self, *pargs, **kargs)
        self.sql_wrapper = TextWrapper(width=100,
                                       initial_indent=' ' * 15 + 'sql> ',
                                       subsequent_indent=' ' * 20)

    def format(self, record):
        fmt = logging.Formatter.format(self, record)
        wrapped_text = "{0}".format(self.sql_wrapper.fill(fmt))
        return wrapped_text

# sqlalchemy engine logger
engine_log = logging.getLogger('sqlalchemy.engine')
root_log = logging.getLogger()


def set_root_logger(level=logging.DEBUG, log_class=logging.StreamHandler):
    # log all debug messages
    # pull the root logger and set it's logging to *level*
    # root = logging.getLogger()
    root_log.setLevel(level)

    h = log_class()
    root_log.addHandler(h)


def set_sql_logger(level=logging.DEBUG, log_class=logging.StreamHandler):
    # setup indented logging for SQL output
    h2 = log_class()
    formatter = WrappedFormatter("%(message)s")
    h2.setFormatter(formatter)
    # For SQL log, INFO is better than DEBUG
    if level == logging.DEBUG:
        engine_log.setLevel(logging.INFO)
    else:
        engine_log.setLevel(logging.ERROR)
    engine_log.addHandler(h2)
    # avoid repeat log entries by stopping propagation
    # of the engine log
    # we're handling it with the indented logger above
    engine_log.propagate = False


# TODO: change thie default level to ERROR and always
# enable logging
def default_debug_log(level=logging.DEBUG, log_class=logging.StreamHandler):
    set_root_logger(level, log_class)
    set_sql_logger(level, log_class)


def enable_sql_log():
    '''Function to turn on debug SQL output for SQLAlchemy'''
    engine_log.setLevel(logging.INFO)


def disable_sql_log():
    '''Function to turn off debug SQL output for SQLAlchemy'''
    engine_log.setLevel(logging.ERROR)


class LogPoint(object):
    '''
    WSGI middleware to output a log message before and after this point in
    the wsgi pipeline
    '''
    def __init__(self, application, begin_message="start", end_message="end",
                 width=79, fillchar='-'):
        self.begin_message = begin_message
        self.end_message = end_message
        self.application = application
        self.log = '{{0:{0}^{1}}}'.format(fillchar, width)

    def __call__(self, environ, start_response):
        log.debug(self.log.format(' {0} '.format(self.begin_message)))
        resp = self.application(environ, start_response)
        log.debug(self.log.format(' {0} '.format(self.end_message)))
        return resp

if __name__ == '__main__':
    unittest.main()
