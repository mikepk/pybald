#!/usr/bin/env python
# encoding: utf-8
# __init__.py
'''
Pybald
======

An MVC-like framework using many best-of-breed components (i.e. webob, sqlalchemy).

(c) 2015 Michael Kowalchik
MIT License, see LICENSE file
'''
import imp
import sys
import os
from pybald.util.context import AppContext
import logging
from .default import default_config
from collections import namedtuple
log = logging.getLogger(__name__)

__version__ = '0.4.0-dev'


def build_config(root_path='.', filename='project.py'):
    filename = os.path.join(root_path, filename)
    config_module = imp.new_module("config")
    config_module.__dict__.update(default_config)
    with open(filename) as config_file:
        exec(compile(config_file.read(), filename, 'exec'), config_module.__dict__)
    return config_module


class Unconfigured(object):
    def __getattr__(self, key):
        raise RuntimeError("Pybald is not configured, you must run "
            "pybald.configure() before context.{0} can be used".format(key))


class DefaultApp(dict):
    def __init__(self, *pargs, **kargs):
        self.register('config', {})
        # self.register('models', Unconfigured())
        # self.register('engine', Unconfigured())
        self.register('controller_registry', [])
        # self.register('model_registry', [])
        self.default = True
        super(DefaultApp, self).__init__(*pargs, **kargs)

    def __getattr__(self, key):
        if key in ('models', 'engine', 'metdata'):
            raise RuntimeError("Pybald is not configured, you must run "
            "pybald.configure() before context.{0} can be used".format(key))
        else:
            return super(DefaultApp, self).__getattr__(key)

    def register(self, key, value):
        self[key] = value
        setattr(self, key, self[key])

# unconfigured application stack context
context = AppContext()
# register the context as a module
sys.modules['pybald.context'] = context
# push the default placeholder app onto the context stack
# the default allows for temporary storage of elements required
# for bootstrapping (and eliminates some sequencing requirements
# for configuration)
context._push(DefaultApp())

# the template engine and database session are built at config time
context_template = '''
from pybald.core.templates import TemplateEngine
from pybald.db.db_engine import create_session, create_engine, create_metadata, create_dump_engine
from pybald.util.command_line import start
from pybald.core.models import ContextBoundModels

render = TemplateEngine()
dump_engine = create_dump_engine()
models = ContextBoundModels()

def register(key, value):
    globals()[key] = value

'''


def configure(name=None, config_file=None, config_object=None):
    '''
    Generate a dynamic context module that's pushed / popped on
    the application context stack.
    '''
    if name is None and config_file is None and config_object is None:
        log.warning("Warning: Using current path for the config file")
    mod = sys.modules.get(name)
    # if mod is not None and hasattr(mod, '__file__'):
    try:
        root_path = os.path.dirname(os.path.abspath(mod.__file__))
    except AttributeError:
        root_path = os.getcwd()

    if root_path not in sys.path:
        sys.path.insert(1, root_path)

    if config_object:
        # create a named tuple that's the combo of default plus input dict
        keys = set(default_config.keys()) | set(config_object.keys())
        ConfigObject = namedtuple("ConfigObject", keys)
        config = ConfigObject(**dict(list(default_config.items()) + list(config_object.items())))
    elif config_file:
        try:
            config = build_config(root_path=root_path, filename=config_file)
        except IOError:
            log.exception("Config Error:\nFile Error or File not found\n{0}".format(config_file))
            sys.exit(1)
    else:
        try:
            config = build_config(root_path=root_path, filename='project.py')
            log.warning("Found project.py in default path, using for the config file")
        except IOError:
            ConfigObject = namedtuple("ConfigObject", default_config.keys())
            config = ConfigObject(**default_config)
            log.warning("No config file, using default pybald configuration")

    new_context = imp.new_module("context")
    # new_app._MODULE_SOURCE_CODE = app_template
    # new_app.__file__ = "<string>"
    if context._proxied() and hasattr(context._proxied(), 'default'):
        # if we're at the root, consume any placeholder values
        # placeholder = context._proxied()
        placeholder = context._pop()
        new_context.__dict__.update(placeholder)
    else:
        new_context.__dict__['controller_registry'] = []
        # new_context.__dict__['model_registry'] = []
    # always set the runtime config
    new_context.__dict__['path'] = root_path
    new_context.__dict__['config'] = config
    new_context.__dict__['name'] = name
    new_context.__dict__['__file__'] = None
    # new_context.__dict__['__path__'] = None
    # now execute the app context with this config
    context._push(new_context)
    exec(compile(context_template, '<string>', 'exec'), new_context.__dict__)
    return new_context

