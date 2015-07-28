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

class AppAttributeProxy(object):
    def __init__(self, app, attribute):
        self.app = app
        self.attribute = attribute

    def __getattr__(self, attr):
        return getattr(getattr(self.app, "_"+self.attribute), attr)
        # return getattr(self.app, "_"+attr)

    def __repr__(self):
        try:
            return repr(getattr(self.app, "_"+self.attribute))
        except (TypeError, AttributeError):
            return str(self)


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
    new_app.__dict__['_config'] = config
    new_app.__dict__['_class_registry'] = []
    new_app.__dict__['_model_registry'] = []
    new_app.__dict__['config'] = AppAttributeProxy(app, 'config')
    new_app.__dict__['class_registry'] = AppAttributeProxy(app, 'class_registry')
    new_app.__dict__['model_registry'] = AppAttributeProxy(app, 'model_registry')
    # now execute the app context with this config
    exec app_template in new_app.__dict__
    return app
