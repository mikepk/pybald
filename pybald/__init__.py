#!/usr/bin/env python
# encoding: utf-8
# __init__.py
'''
Pybald
======

An MVC-like framework using many best-of-breed components (i.e. webob,
sqlalchemy).

(c) 2015 Michael Kowalchik
MIT License, see LICENSE file
'''
import types
import sys
import os
from pybald.util.context import AppContext
import logging
from .default import default_config
from collections import namedtuple
log = logging.getLogger(__name__)

__version__ = '0.5.8'


def read_config_module(root_path='.', filename='project.py'):
    '''Read a configuration module and append it's path to sys.path'''
    # since the config module may have relative imports
    # add the _config files_ path to root before executing the config
    if root_path not in sys.path:
        sys.path.insert(1, root_path)
    filename = os.path.join(root_path, filename)
    config_module = types.ModuleType("config")
    config_module.__dict__['__file__'] = filename
    config_module.__dict__['path'] = root_path
    with open(filename) as config_file:
        exec(compile(config_file.read(), filename, 'exec'),
             config_module.__dict__)
    return config_module


class Unconfigured(object):
    def __getattr__(self, key):
        raise RuntimeError("Pybald is not configured, you must run "
                           "pybald.configure() before context.{0} can"
                           " be used".format(key))


class DefaultApp(dict):
    def __init__(self, *pargs, **kargs):
        self.register('config', {})
        self.register('controller_registry', [])
        # self.register('model_registry', [])
        self.unconfigured = True
        super(DefaultApp, self).__init__(*pargs, **kargs)

    # def __getattr__(self, key):
    #     if key in ('models', 'engine', 'metdata'):
    #         raise RuntimeError("Pybald is not configured, you must run "
    #                            "pybald.configure() before context.{0} can"
    #                            " be used".format(key))
    #     else:
    #         return super(DefaultApp, self).__getattr__(key)

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
from pybald.util.command_line import start
from pybald.core.models import ContextBoundModels
from pybald.db.db_engine import create_dump_engine

render = TemplateEngine()
dump_engine = create_dump_engine()
if config.database_engine_uri:
    models = ContextBoundModels()
    db = models.db
else:
    models = Unconfigured()
    db = Unconfigured()

def register(key, value):
    globals()[key] = value

'''


def create_config_dict_from_module(module):
    '''Converts a module into a dictionary filtering out common module
    level attributes'''
    return {key: getattr(module, key) for key in module.__dict__.keys() if
            not key.startswith('_') and key not in ('sys', 'os')}


def create_config_object(config_object):
    '''Convert a config dictionary to a config object named tuple
    and combines it with the default configuration dictionary.'''
    keys = set(default_config.keys()) | set(config_object.keys())
    ConfigObject = namedtuple("ConfigObject", keys)
    return ConfigObject(**dict(list(default_config.items()) +
                               list(config_object.items())))


def bootstrap(bootstrap_file=None):
    '''Execute the python file passed in. It's assumed that the bootstrap
    python module file will execute configure() before returning although
    not strictly necessary

    This is intended for complicated projects that need to do a lot of
    dynamic stuff before configuring the project. It's primarily a convenience
    hook that sets the sys.path to the current working directory before
    executing the module import.

    Use of this method should be rare, ask yourself if you really need it :)
    '''
    # since bootstrap can be anywhere, add bootstrap to sys.path as well
    if os.getcwd() not in sys.path:
        sys.path.insert(1, os.getcwd())
    possible_root_path = os.getcwd()
    root_path, filename = os.path.split(os.path.join(possible_root_path,
                                                     bootstrap_file))
    if root_path not in sys.path:
        sys.path.insert(1, root_path)
    filename = os.path.join(root_path, filename)
    bootstrap_module = types.ModuleType("bootstrap")
    bootstrap_module.__dict__['__file__'] = filename
    with open(filename) as bootstrap_file:
        exec(compile(bootstrap_file.read(), filename, 'exec'),
             bootstrap_module.__dict__)
    return bootstrap_module


def configure(name=None, config_file=None, config_object=None, **kargs):
    '''
    Generate a dynamic context module that's pushed / popped on
    the application context stack.
    '''
    script_name = sys.argv[0]
    # always add current working directory to the path regardless
    # was trying to avoid this but too much path munging happening
    if os.getcwd() not in sys.path:
        sys.path.insert(1, os.getcwd())

    if config_object:
        if 'project_name' not in config_object:
            config_object['project_name'] = script_name
        # create a named tuple that's the combo of default plus input dict
        root_path = config_object['path'] = config_object.get('path',
                                                              os.getcwd())
        config = create_config_object(config_object)
        # add root path to config?
    elif config_file:
        # possible root path if relative filename specified
        possible_root_path = os.getcwd()
        root_path, filename = os.path.split(os.path.join(possible_root_path,
                                                         config_file))
        try:
            config_module = read_config_module(root_path=root_path,
                                               filename=filename)
        except IOError:
            log.exception("Config Error:\n"
                          "File Error or File not "
                          "found\n{0}".format(config_file))
            sys.exit(1)
        config = create_config_object(create_config_dict_from_module(config_module))
    elif kargs:
        if 'project_name' not in kargs:
            kargs['project_name'] = script_name

        root_path = kargs['path'] = kargs.get('path',
                                              os.getcwd())
        config = create_config_object(kargs)
    else:
        root_path = os.getcwd()
        log.warning("Warning: Using current path for the config "
                    "file {0}".format(root_path))
        if root_path not in sys.path:
            sys.path.insert(1, root_path)
        try:
            config_module = read_config_module(root_path=root_path,
                                               filename='project.py')
            log.warning("Found project.py in default path, "
                        "using for the config file")
        except IOError:
            config = create_config_object(default_config)
            log.warning("No config file, using default pybald configuration")
        else:
            config = create_config_object(create_config_dict_from_module(config_module))

    # if the discovered root_path is not in sys.path, add it in the least ugly
    # way possible
    if root_path not in sys.path:
        sys.path.insert(1, root_path)

    if config.debug:
        from pybald.core.logs import default_debug_log
        default_debug_log()

    new_context = types.ModuleType("context")

    if context._proxied() and hasattr(context._proxied(), 'unconfigured'):
        # if we're at the root, consume any placeholder values
        placeholder = context._pop()
        new_context.__dict__.update(placeholder)
    else:
        new_context.__dict__['controller_registry'] = []
    # always set the runtime config
    new_context.__dict__['path'] = root_path
    new_context.__dict__['config'] = config
    new_context.__dict__['name'] = name
    new_context.__dict__['__file__'] = None
    new_context.__dict__['Unconfigured'] = Unconfigured
    # new_context.__dict__['__path__'] = None
    # now execute the app context with this config
    context._push(new_context)
    exec(compile(context_template, '<string>', 'exec'), new_context.__dict__)
    return new_context
