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


def build_config(root_path='.', filename='project.py'):
    # TODO FIXME - this hardcoded path needs to be found somehow
    filename = os.path.join(root_path, filename)
    config_module = imp.new_module("config")
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), config_module.__dict__)
    except IOError:
        log.exception('Problem loading config file {0}'.format(filename))
        raise
    return config_module

# unconfigured application stack context
app = AppContext()
sys.modules['pybald.app'] = app

class DefaultApp(dict):
    def __init__(self, *pargs, **kargs):
        self['config'] = {}
        self['controller_registry'] = []
        self['model_registry'] = []
        self.config = self['config']
        self.controller_registry = self['controller_registry']
        self.model_registry = self['model_registry']
        self.default = True
        super(DefaultApp, self).__init__(*pargs, **kargs)

app._push(DefaultApp())

app_template = '''
from pybald.core.templates import TemplateEngine
render = TemplateEngine()

from pybald.db import models
'''



def configure(name, config_file=None):
    '''
    Generate a dynamic app module that's pushed / popped on
    the application context stack.
    '''
    mod = sys.modules.get(name)
    # if mod is not None and hasattr(mod, '__file__'):
    root_path = os.path.dirname(os.path.abspath(mod.__file__))

    if config_file:
        config = build_config(root_path=root_path, filename=config_file)
    else:
        config = build_config(root_path=root_path, filename='project.py')

    new_app = imp.new_module("app")
    if hasattr(app._proxied(), 'default'):
        placeholder = app._pop()
        new_app.__dict__.update(placeholder)
    else:
        new_app.__dict__['controller_registry'] = []
        new_app.__dict__['model_registry'] = []
    # always set the runtime config
    new_app.__dict__['path'] = root_path
    new_app.__dict__['config'] = config
    # now execute the app context with this config
    app._push(new_app)
    exec(compile(app_template, '<string>', 'exec'), new_app.__dict__)
    return new_app
