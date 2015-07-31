#!/usr/bin/env python
# encoding: utf-8
# __init__.py
#
# Created by mikepk on 2009-07-24.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.
import imp
import sys
import os
from pybald.util.context import AppContext
import logging
log = logging.getLogger(__name__)

__version__ = '0.4-dev'


def build_config(filename='project.py'):
    filename = os.path.join('/usr/share/ps/temp', filename)
    d = imp.new_module("config")
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
    except IOError:
        log.exception('Problem loading config file {0}'.format(filename))
        raise
    return d

# unconfigured application stack context
app = AppContext()
sys.modules['pybald.app'] = app

app_template = '''
from pybald.app import config as project
from pybald.core.templates import TemplateEngine
render = TemplateEngine()

from pybald.db import models
'''

def pybald_app(name, config):
    '''
    Generate a dynamic app module that's pushed / popped on
    the application context stack.
    '''
    new_app = imp.new_module("app")
    app._set_proxy(new_app)
    new_app.__dict__['config'] = config
    new_app.__dict__['controller_registry'] = []
    new_app.__dict__['model_registry'] = []
    # now execute the app context with this config
    exec(compile(app_template, '<string>', 'exec'), new_app.__dict__)
    return new_app
