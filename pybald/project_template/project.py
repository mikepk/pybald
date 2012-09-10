#!/usr/bin/env python
# encoding: utf-8
"""
project.py

A module to hold project specific members and configuration.
"""
import sys
import os

# Configure the project path and package name
path = os.path.dirname( os.path.realpath( __file__ ) )
toplevel = os.path.split(path)[0]
package_name = os.path.split(path)[-1]

# project name (otherwise default to the the project's path name)
project_name = package_name

# debug information
debug = True
env_name = "Development"

# Memcached, localhost only at the moment
memcached_clients = ['127.0.0.1:11211']

# Feature Flags
# =============================

# options that are passed into the view
# directly
# page_options = {'analytics' : False}
page_options = {}

# additional template helpers to add to the context for all tempaltes
template_helpers = ['from pybald.core import page']

# route email to a local smtp server
smtp_config = {"smtp_server":"127.0.0.1",
               "smtp_port":1025,
               "use_tls":False,
               "AuthUser":"USER@HOST",
               "AuthPass":""}

# sqlalchemy engine string examples:
# mysql -         "mysql://{user}:{password}@{host}/{database}"
# postgres - postgresql://{username}:{password}@{host}:{port}/{database}'
# sqllite -       "sqlite:///{filename}"
# sqllite mem -   "sqlite:///:memory:"

# local database connection settings
# default to a sqllite file database based on the project name
database_engine_uri_format = 'sqlite:///{filename}'
db_config = {'filename':os.path.join(path,
             '{project}.sqlite'.format(project=project_name))}

# create the db engine uri
database_engine_uri = database_engine_uri_format.format(**db_config)

#sqlalchemy engine arguments
# database_engine_args = {'pool_recycle':3600,
#                         'pool_size':50,
#                         'max_overflow':9,
#                         'encoding':'utf-8' }
database_engine_args = {}

# use SQLAlchemy's Schema Reflection on all models
# this will load the table definitions on startup and define your models
schema_reflection = False

# Arguements applied to all SQLAlchemy tables
# useful mysql global args: {'mysql_engine':'InnoDB', 'mysql_charset':'utf8'}
global_table_args = {}

# check for the environment file, if there, override options
# with the environment
if os.path.isfile(os.path.join(path, "environment.py")):
    from environment import *
    sys.stderr.write("LOADED ENVIRONMENT: {0}\n".format(env_name))


import memcache
# load memcached after the environment is loaded
mc = memcache.Client(memcached_clients, debug=0)

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

from pybald.core.logs import enable_sql_log
if debug:
    enable_sql_log()

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