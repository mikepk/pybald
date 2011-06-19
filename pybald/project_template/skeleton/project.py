
import sys
import os

# debug information
debug = True
env_name = "Default"

# import memcache
# mc = memcache.Client(['127.0.0.1:11211'], debug=0)

# using eventlet (co-routines / greenthreads)
green = False

# temporary until I have pybald be installable
pybald_path = '/usr/share/smarterer/pybald' # <- Must set pybald path
project_name = "skeleton"

# define project routes for the URL mapper
def set_routes(rmap):
    '''Simple function to define routes. A routes map object should be passed in.'''

    # the order of the routes is important, more specific should come before
    # more generic

    if not rmap:
        raise Exception("No Routes Mapper")

    # the order of the routes is important, more specific should come before
    # more generic

    # Mostly static content mapped to the content controller
    with rmap.submapper(controller="content", action="render") as m:
        m.connect('about','/about', template='about')


    # sample RESTful mapping
    # rmap.resource("question", "questions", path_prefix="/quizzes/{quiz_id}")
    # rmap.resource("quiz", "quizzes")

    # home
    rmap.connect('home','/', controller='home')

    # generic pattern
    rmap.connect('/{controller}/{action}/{id}')
    rmap.connect('/{controller}/{action}')
    rmap.connect('/{controller}')

    if debug:
        print rmap

def get_engine():
    '''Get sqlalchemy engine string.
    Examples:
      mysql -         "user:passwd@host/dbname"
      sqllite -       "sqlite:///filename"
      sqllite (alt) - "sqlite:///%s" % os.path.join(get_path(),'%s.sqlite' % project_name)
      sqllite mem -   "sqlite:///:memory:"
    '''
    return "sqlite:///%s" % os.path.join(get_path(),'%s.sqlite' % project_name)

def get_engine_args():
    '''SqlAlchemy engine arguments'''
    options = {'pool_recycle':3600,
                'pool_size':10,
                'encoding':'utf-8' }
    if debug:
        # show all sqlalchemy queries in log
        options['echo'] = True
    return options

# Configure the project path
def get_path():
    '''Return the project path.'''
    return os.path.dirname( os.path.realpath( __file__ ) )

def get_toplevel():
    '''Return the outer project path.'''
    return os.path.split(get_path())[0]

# check for the environment file, if there, override options
# with the environment
if os.path.isfile(os.path.join(get_path(), "environment.py")):
    from environment import *
    print "LOADED ENVIRONMENT: %s" % env_name

# HACK: this allows project.X to return a default of None when
# undefined attributes are called (or setup from environment)
class ConfigWrapper(object):
  def __init__(self, wrapped):
    self.wrapped = wrapped
  def __getattr__(self, name):
    # Some sensible default?
    return getattr(self.wrapped, name, None)


# Runs the project console. Allows interacting with the models and controllers.
if __name__ == '__main__':
    # set the sys.modules project entry to this file
    # wrapped in the ConfigWrapper to avoid double import
    sys.modules['project'] = ConfigWrapper(sys.modules['__main__'])

    # Where is this module? set the project path accordingly
    project_path = os.path.dirname( os.path.realpath( __file__ ) )
    sys.path.append(project_path)
    sys.path.append(pybald_path)
    sys.path.append(get_toplevel())

    import pybald
    import project
    from pybald.core.Console import Console
    import app.controllers
    from app.models import *
    # Fire up the console with the project, controllers, and models defined.
    console = Console(locals=locals())
    console.interact('Welcome to the pybald interactive shell\n ** %s **\n' % project_name )
else:
    # Sets this module's entry in modules to be wrapped by the getattr
    # hack. Allows config options to be tested without an exception.
    sys.modules[__name__] = ConfigWrapper(sys.modules[__name__])
