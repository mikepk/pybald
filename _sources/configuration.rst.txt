Configuration
===============

All pybald applications must be configured early in the lifecycle of the application (generally before any controllers or models are defined). To configure an application, import the pybald module and run the ``configure`` function.

.. sourcecode:: python

    import pybald

    # configure our pybald application
    pybald.configure(debug=True)

There are several ways to configure a pybald application, but they all consist of building a set of key/value pairs to define how the application will run. In the example above, ``debug=True`` was passed as a key/value pair turning on debug.

Generally the config will be where you define things like:

 * whether the project is in debugging mode or not
 * logging directives
 * if using a database the database kind, host, port, username and password
 * paths to static files, templates, etc...
 * template helpers to load into all templates
 * other server configurations, like SMTP servers, search servers, etc...

Defaults
--------

Pybald has a set of default configuration values that will always be used as the basis for a config. This allows starting a simple pybald application with very little configuration. The defaults are stored in the ``pybald.default`` module as a dictionary. This default dictionary will automatically be combined with any user supplied values to create the final configuration.

.. sourcecode:: pycon

    >>> from pybald.default import default_config
    >>> from pprint import pprint
    >>> pprint(default_config)
    {'DEFAULT_PROTOCOL': 'http',
     'STATIC_SOURCES': None,
     'USE_CDN': False,
     'cache_path': 'tmp/viewscache',
     'database_engine_args': {},
     'database_engine_uri': '',
     'debug': True,
     'email_errors': False,
     'env_name': 'Default',
     'global_table_args': {},
     'host_name': 'localhost',
     'page_options': {},
     'path': '',
     'project_name': None,
     'schema_reflection': False,
     'smtp_config': {},
     'static_path': 'public',
     'template_default_filters': ['h', 'unicode'],
     'template_default_helpers': ['from pybald.core.helpers import img, link, humanize, HTMLLiteral as literal, url_for',
                                  'from pybald.core import page'],
     'template_filesystem_check': True,
     'template_helpers': [],
     'template_path': 'app/views'}

You don't need to know what all of the defaults mean right now, but it's useful to be able to list them all and get a sense of what's available.

There's no limit to what values you can add to a config file. If you have project specific configuration variables you'd like to add, they will be included into the config.

Methods of Configuring
----------------------

While there are several ways to configure a Pybald application, generally only one should be used at a time. Mixing config methods (keyword arguments and file for example) is not currently supported.

Keyword Argument
~~~~~~~~~~~~~~~~

For the simplest projects, keyword arguments passed to the configure function can be used. This was the way ``debug=True`` was set on the configuration for the sample application.

.. sourcecode:: python

    import pybald

    # configure our pybald application
    pybald.configure(debug=True)


For larger projects, passing all the configuration options as keyword arguments becomes awkward so as a project grows, generally one of the other methods for configuration is used.

Config Dictionary
~~~~~~~~~~~~~~~~~

You can also configure a pybald application by building a dictionary of options and passing it to the configure function with the ``config_object`` keyword argument.

.. sourcecode:: python

    import pybald

    # configure our pybald application
    pybald.configure(config_object={'debug': True})


Config File (Module)
~~~~~~~~~~~~~~~~~~~~

You can also configure a Pybald application by using a configuration file. Pybald configuration files are simple python modules. You can create a python module in the main project path that contains the variables you wish to use for your configuration. Traditionally this file is named ``project.py`` and lives in the root path of your project but it can be named anything. You can specify a python module and path to use as the config file by using the ``config_file`` keyword argument.

.. sourcecode:: python

    import pybald

    # configure our pybald application
    pybald.configure(config_file='project.py')

If no config options or keywords are passed to the ``configure`` function, pybald will attempt to load a config file named ``project.py`` from the project path. If no file with that name is present, then the default configuration will be used.

.. sourcecode:: python

    import pybald

    # configure our pybald application, nothing specified
    # so attempt to load a project.py file if present
    pybald.configure()

This will attempt to load a project.py file if present.

Sample project.py
*****************

Project.py files generally look like a list of variable declarations. This doesn't mean you can't run python code or do dynamic things with the config options, in fact this is the main use case for using a python module for configuration rather than a static file format like an ini file. For example, one common use case for this pattern is to dynamically generate the database URI for a database connection using string interpolation. Another useful trick is to have a base project.py file that includes an environment.py file with environmental (production, test, development) specific values.

.. sourcecode:: python

    sample_config = True
    env_name = "SampleTestProjectEnvironment"
    template_path = "sample_project/templates"
    cache_path = None
    project_name = "Sample Project"
    debug = True
    BUNDLE_SOURCE_PATHS = ['tests/sample_project/front_end', 'tests/sample_project/sass']
    database_engine_uri = 'sqlite:///:memory:'


The Pybald context
------------------

.. sidebar:: About Contexts

    Under the covers, the Pybald context is a *Stacked Object Proxy* using a python threadlocal. This means that anywhere a reference to ``context`` is found, that reference is actually a proxy to the underlying context. When the context is changed, it is changed for all references.

    Why? The reason for this is to support running multiple Pybald applications simultaneously. Each call to configure creates a new context and pushes the current context onto the context stack. When one pybald application calls a second Pybald application in the same interpreter, it must handle popping and pushing the context for the 'child' application onto the stack before beginning execution of the second Pybald app. This allows the different applications to share code but not configuration.

    This is a more advanced use case, but it does have one important ramification if you're using the simple case, you should make sure that ``pybald.configure()`` is only called **once** for any application. *Every* call to configure will create an entirely new application context and push it onto the context stack. This may lead to strange behaviors or bugs if not careful.

Regardless of the method used, once a Pybald application is configured a *context* is created. The configure function call creates the context and an immutable ``ConfigObject`` and attaches it to the context. The ConfigObject is the combination of the default configuration values and any user supplied values.

A Pybald ``context`` represents the configuration and any globally accessible state for the application. Once an application is configured, importing the context from pybald will give you access to this shared context. This allows you to have access to the configuration from multiple python modules without having to explicitly pass references to the context.

Importing ``context`` from pybald gives you access to the current application's configuration and any shared resource (like caching or database connections).

.. sourcecode:: pycon

    >>> from pybald import context
    >>> context.config
    ConfigObject(project_name='sample.py', BUNDLE_ASSETS=False, global_table_args={}, USE_CDN=False, BUNDLE_OUTPUT_PATH='/min', email_errors=False, debug=True, cache_path='tmp/viewscache', template_default_helpers=['from pybald.core.helpers import img, link, humanize, HTMLLiteral as literal, url_for', 'from pybald.core import page'], path='/home/username/projects/sample', template_filesystem_check=True, database_engine_uri='', database_engine_args={}, template_path='app/views', BUNDLE_SOURCE_PATHS=['/front_end', '/sass'], BUNDLE_FILTER_OPTIONS=[], env_name='Default', page_options={}, host_name='localhost', smtp_config={}, template_helpers=[], BUNDLE_AUTO_BUILD=True, template_default_filters=['h', 'unicode'], schema_reflection=False, static_path='public')
    >>> context.config.debug
    True

Common config arguments
------------------------

Runtime
~~~~~~~

The most common runtime configuration arguments are ``project_name``, ``path``, ``env_name`` and ``debug``.

* ``project_name`` an identifier for the current project, mostly informational and is used for storing per project comand line history
* ``path`` the root of the current application. This root path is used when determining any relative paths for other configuration options.
* ``env_name`` a meaningful 'environment' name useful for identifying the current running environment. Again mostly informational but is sometimes used for triggering behaviors (i.e. only instrument when in production)
* ``debug`` whether the application runs in debug mode or not. Debug mode generally has chattier log output as well as changing the way some component behave. One example is the error handler, when in debug mode, will return a nicely formatted stack trace on exceptions, wheras when not in debug mode a user facing error message is returned.

Templates
~~~~~~~~~

There are a few configuration options that change the way the templating system behaves. These include:

* ``cache_path`` - where compiled (Mako) templates will be stored
* ``template_default_helpers`` - python functions to import into all templates to provide functions like link generation. These functions will be available in all templates and can be used directly (see the section on templating).
* ``template_filesystem_check`` - when True, the template engine will check for changes to the underlying template files on every load, otherwise the cached version will always be used.
* ``template_path`` - the path where project templates will be stored. Usually this is a relative path the the project's root path.
* ``template_default_filters`` - the default filters to run on all template output. By default, the HTML escape filter ``h`` which escapes all output to avoide XSS type attacks and ``unicode`` are used to make sure all output returns as unicode. You can dynamically add any filters to ouptut in templates, but these defaults will always be applied. Note: think hard before you decide to remove the html escape filter since that's the root of many security problems!

Databases
~~~~~~~~~

Database configuration is done via SQLAlchemy which uses a URI following `RFC-1738 <https://www.ietf.org/rfc/rfc1738.txt>`_. The uri is in the config variable `database_engine_uri`. Generally pybald projects use some string interpolation to create these URLs from configuration dictionaries. This allows creating different ``environments`` with different config dictionaries but keep the same underlying config connection string.

Here is a sample ``project.py`` with a block to define a simple sqllite database as the database URI. Additionally it contains comments to show some other common URI patterns. These patterns are presented to show how one might create a mysql or postgres connection.


.. sourcecode:: python

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

