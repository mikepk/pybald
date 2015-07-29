#!/usr/bin/env python
# encoding: utf-8
# __init__.py
#
# Created by mikepk on 2009-07-24.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.
import imp
import sys
from pybald.util.context import AppContext

__version__ = '0.4-dev'

# unconfigured application stack context
app = AppContext()
sys.modules['pybald.app'] = app


def pybald_app(name, config):
    '''
    Generate a dynamic app module that's pushed / popped on
    the application context stack.
    '''
    app_template = '''
from pybald.app import config as project
from pybald.core.templates import TemplateEngine
render = TemplateEngine()

from pybald.db import models
'''
    new_app = imp.new_module("app")
    app._set_proxy(new_app)
    new_app.__dict__['config'] = config
    new_app.__dict__['class_registry'] = []
    new_app.__dict__['model_registry'] = []
    # now execute the app context with this config
    exec app_template in new_app.__dict__
    return app
