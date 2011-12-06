#!/usr/bin/env python
# encoding: utf-8
"""
project.py

A module to hold project specific members and configuration.
"""
import sys
import os
import logging

# debug information
debug = True
env_name = "Development"

# using eventlet (co-routines / greenthreads)
# green = False

# options that are passed into the view
# directly
page_options = {'analytics' : False}

path = os.path.dirname( os.path.realpath( __file__ ) )
# Project name
toplevel = os.path.split(path)[0]
package_name = os.path.split(path)[-1]
project_name = package_name

# route email to a local smtp server
smtp_config = {"smtp_server":"127.0.0.1",
               "smtp_port":1025,
               "use_tls":False,
               "AuthUser":"root@localhost",
               "AuthPass":""}

# sqlalchemy engine string examples:
# mysql -         "mysql://user:passwd@host/dbname"
# sqllite -       "sqlite:///filename"
# sqllite (alt) - "sqlite:///%s" % os.path.join(path,'%s.sqlite' % project_name)
# sqllite mem -   "sqlite:///:memory:"

# local db connection settings
# default to a sqllite file database based on the project name
db_config = {'filename':os.path.join(path,
             '{project}.sqlite'.format(project=project_name))}
database_engine_uri = "sqlite:///{filename}".format(**db_config)

#sqlalchemy engine arguments
database_engine_args = {}
    # MySQL table arguments
    # 'pool_recycle':3600,
    # 'pool_size':50,
    # 'max_overflow':9,
    # 'encoding':'utf-8' }

# use SQLAlchemy's Schema Reflection on all models
# this will load the table definitions on startup and define your models
# schema_reflection = False

# mysql global table arguments
# global_table_args = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}

# FIXME - This needs to be cleaned up. Not sure what the design for pybald
# model logging should be
def set_logging():
    '''Temporary method to make logging optional.'''
    # experimental logging handling
    from textwrap import TextWrapper
    class WrappedStream(object):
        def __init__(self):
            self.sql_wrapper = TextWrapper(width=100,
                                           initial_indent=' '*15+'sql> ',
                                           subsequent_indent=' '*20)
        def write(self, text):
            wrapped_text = "{0}\n".format(self.sql_wrapper.fill(text))
            sys.stderr.write(wrapped_text)

        def flush(self, *pargs, **kargs):
            pass

    engine_log = logging.getLogger('sqlalchemy.engine')
    logging.getLogger('sqlalchemy.orm.unitofwork').setLevel(logging.ERROR)

    h = logging.StreamHandler(WrappedStream())
    engine_log.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")
    h.setFormatter(formatter)
    engine_log.addHandler(h)


def stop_logging():
    logging.disable(logging.WARN)

def get_toplevel():
    '''Return the outer project path.'''
    return toplevel

package_name = os.path.split(path)[-1]
models_module = "{0}.app.models".format(package_name)
controllers_module = "{0}.app.controllers".format(package_name)

# check for the environment file, if there, override options
# with the environment
if os.path.isfile(os.path.join(path, "environment.py")):
    from environment import *
    sys.stderr.write("LOADED ENVIRONMENT: {0}\n".format(env_name))

# HACK: this allows project.X to return a default of None when
# undefined attributes are called (or setup from environment)
class ConfigWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __getattr__(self, name):
        # Some sensible default?
        return getattr(self.wrapped, name, None)
    def __dir__(self):
        return dir(self.wrapped)

if debug:
    set_logging()

# Runs the project console. Allows interacting with the models and controllers.
if __name__ == '__main__':
    # set the sys.modules project entry to this file
    # wrapped in the ConfigWrapper to avoid double import
    sys.modules['project'] = ConfigWrapper(sys.modules['__main__'])
    from pybald.core.console import Console
    console = Console(project_name=project_name, package_name=package_name)
    console.run()
else:
    # Sets this module's entry in modules to be wrapped by the getattr
    # hack. Allows config options to be tested without an exception.
    sys.modules[__name__] = ConfigWrapper(sys.modules[__name__])
