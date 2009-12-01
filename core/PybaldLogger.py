#!/usr/bin/env python
# encoding: utf-8
"""
PybaldLogger.py

Created by mikepk on 2009-12-01.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""

import sys
import os
import unittest

import logging
import logging.handlers        

class PybaldLogger:
    def __init__(self,log_file = '/tmp/pybald_log.out'):
        
        LOG_FILENAME = log_file

        # Set up a specific logger with our desired output level
        self.my_logger = logging.getLogger('PyBald')
        self.my_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      LOG_FILENAME, maxBytes=1024*1024*20, backupCount=50)

        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to handler
        handler.setFormatter(formatter)

        self.my_logger.addHandler(handler)

    def write(self,msg):
        if msg == '\n':
            return
        # msg = msg.rstrip()
        # self.my_logger.debug(repr(msg))
        self.my_logger.debug(msg)


class PybaldLoggerTests(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()