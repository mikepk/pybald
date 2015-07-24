#!/usr/bin/env python
# encoding: utf-8
# __init__.py
#
# Created by mikepk on 2009-07-24.
# Copyright (c) 2009 Michael Kowalchik. All rights reserved.
import imp
import sys

__version__ = '0.4-dev'

class AppObject(object):
    pass

from pybald.config import project

from paste.registry import StackedObjectProxy



# >>> import imp
# >>> foo = imp.new_module("foo")
# >>> foo_code = """
# ... class Foo:
# ...     pass
# ... """
# >>> exec foo_code in foo.__dict__
# >>> foo.Foo.__module__
# >>> import sys
# >>> sys.modules["foo"] = foo
# >>> from foo import Foo
# <class 'Foo' …>
# >>>

app = StackedObjectProxy()

def pybald_app(name, config):
    '''
    Generate a dynamic app module / namespace that's pushed / popped on
    the application / thread context.
    '''
    project._push_object(config)
    app_template = '''
from pybald.core.templates import TemplateEngine
render = TemplateEngine()

from pybald.db import models
'''
    new_app = imp.new_module("app")
    exec app_template in new_app.__dict__
    app._push_object(new_app)
    sys.modules['pybald.app'] = app
    return app
