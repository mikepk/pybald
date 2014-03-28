#!/usr/bin/env python
# encoding: utf-8
"""
project.py

A module to hold project specific members and configuration.
"""
import sys
import os
from pybald.core.logs import default_debug_log

# Configure the project path and package name
path = os.path.dirname(os.path.realpath(__file__))
toplevel = os.path.split(path)[0]
package_name = os.path.split(path)[-1]

# project name (otherwise default to the the project's path name)
project_name = package_name

# debug information
debug = True
env_name = "Development"

# options that are passed into the views
# directly
page_options = {}

# additional template helpers to add to the context for all templates
template_helpers = ['from pybald.core import page']

# route email to a local smtp server
smtp_config = {"smtp_server": "127.0.0.1",
               "smtp_port": 1025,
               "use_tls": False,
               "AuthUser": "USER@HOST",
               "AuthPass": ""}

# sqlalchemy engine string examples:
# mysql -         "mysql://{user}:{password}@{host}/{database}"
# postgres - postgresql://{username}:{password}@{host}:{port}/{database}'
# sqllite -       "sqlite:///{filename}"
# sqllite mem -   "sqlite:///:memory:"

# local database connection settings
# default to a sqllite file database based on the project name
database_engine_uri_format = 'sqlite:///{filename}'
db_config = {'filename': os.path.join(path,
             '{project}.sqlite'.format(project=project_name))}

# create the db engine uri
database_engine_uri = database_engine_uri_format.format(**db_config)

#sqlalchemy engine arguments
# database_engine_args = {'pool_recycle':3600,
#                         'pool_size':50,
#                         'max_overflow':9,
#                         'encoding':'utf-8' }
database_engine_args = {}

# Arguements applied to all SQLAlchemy tables
# useful mysql global args: {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
global_table_args = {}

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
    default_debug_log()

# Runs the project console. Allows interacting with the models and controllers.
if __name__ == '__main__':
    # import sys
    sys.path.append(toplevel)
    if __package__ is None:
        __import__(package_name, globals(), locals(), [], -1)
        __package__ = package_name

    # set the sys.modules project entry to this file
    # wrapped in the ConfigWrapper to avoid double import
    sys.modules['project'] = ConfigWrapper(sys.modules['__main__'])
    from pybald.util.console import Console

    # load the application!
    from .wsgi.myapp import app

    # now the models registry should be loaded and the additional_symbols
    # added
    from pybald.db.models import Model
    models = dict([(model.__name__, model) for model in Model.registry])

    # create a pybald console around it
    console = Console(project_name=project_name, app=app,
                      additional_symbols=models)
    console.run()
else:
    # Sets this module's entry in modules to be wrapped by the getattr
    # hack. Allows config options to be tested without an exception.
    sys.modules[__name__] = ConfigWrapper(sys.modules[__name__])
