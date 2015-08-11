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
    filename = os.path.join(root_path, filename)
    config_module = imp.new_module("config")
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), config_module.__dict__)
    except IOError:
        log.exception('Problem loading config file {0}'.format(filename))
        raise
    return config_module


class MockEngine(object):
    def __getattr__(self, key):
        raise RuntimeError("Pybald is not configured")


class DefaultApp(dict):
    def __init__(self, *pargs, **kargs):
        self.register('config', {})
        self.register('engine', MockEngine())
        self.register('controller_registry', [])
        self.register('model_registry', [])
        self.default = True
        super(DefaultApp, self).__init__(*pargs, **kargs)

    def register(self, key, value):
        self[key] = value
        setattr(self, key, self[key])

# unconfigured application stack context
app = AppContext()
sys.modules['pybald.app'] = app
# push the default placeholder app onto the context stack
# the default allows for temporary storage of elements required
# for bootstrapping (and eliminates some sequencing requirements
# for configuration)
app._push(DefaultApp())

# the template engine and database session are built at config time
app_template = '''
from pybald.core.templates import TemplateEngine
from pybald.db.db_engine import create_session, create_engine, create_dump_engine
from pybald.util.console import start_console as console
from pybald.util.dev_server import start_dev_server as serve

render = TemplateEngine()
dump_engine = create_dump_engine()
engine = create_engine()
db = create_session(engine=engine)
'''


def configure(name, config_file=None, config_object=None):
    '''
    Generate a dynamic app module that's pushed / popped on
    the application context stack.
    '''
    mod = sys.modules.get(name)
    # if mod is not None and hasattr(mod, '__file__'):
    try:
        root_path = os.path.dirname(os.path.abspath(mod.__file__))
    except AttributeError:
        root_path = os.getcwd()

    if config_object:
        config = config_object
    elif config_file:
        config = build_config(root_path=root_path, filename=config_file)
    else:
        config = build_config(root_path=root_path, filename='project.py')

    new_app = imp.new_module("app")
    new_app._MODULE_SOURCE_CODE = app_template
    if hasattr(app._proxied(), 'default'):
        placeholder = app._pop()
        new_app.__dict__.update(placeholder)
    else:
        new_app.__dict__['controller_registry'] = []
        new_app.__dict__['model_registry'] = []
    # always set the runtime config
    new_app.__dict__['path'] = root_path
    new_app.__dict__['config'] = config
    new_app.__dict__['name'] = name
    # now execute the app context with this config
    app._push(new_app)
    exec(compile(app_template, '<string>', 'exec'), new_app.__dict__)
    return new_app

# aliases for convenience
from pybald.core.controllers import Controller, action
from pybald.core.router import Router
from pybald.core.logs import default_debug_log as debug_log