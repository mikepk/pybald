#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

from webob import Request, Response

import logging
import logging.handlers

class PybaldLogger(object):
    def __init__(self, application=None, log_file='/tmp/pybald.log',
                       level="DEBUG", project_name="Pybald"):
        if application:
            self.application = application
        else:
            # no pipeline so just generate a generic response
            self.applicaion = Response()
        LOG_FILENAME = log_file

        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger(project_name)
        log_level = getattr(logging,level)
        self.my_logger.setLevel(log_level)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME,
                      maxBytes=1024*1024*20,
                      backupCount=10)

        # create formatter
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s...%(message)s")
        # add formatter to handler
        handler.setFormatter(formatter)
        self.my_logger.addHandler(handler)
        self.write("Logger Started - %s" % level)


    def __call__(self,environ,start_response):
        req = Request(environ)
        sys.stdout = self
        sys.stderr = self
        #environ['wsgi.errors'] = self
        #pass through if no exceptions occur
        resp = req.get_response(self.application)
        return resp(environ,start_response)

    def write(self,msg):
        if msg == '\n':
            return
        self.my_logger.info(msg)


class PybaldLoggerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()