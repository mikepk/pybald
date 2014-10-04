Using Pybald
===============

A Quick Note on Naming Conventions
----------------------------------

Pybald tries to bridge the convention over configuration (CoC) approach and the explicit approach to creating a web application. For the basics of the web framework, it tends to favor the CoC approach. Pybald has a few naming conventions that are expected and may cause confusion if not understood.

Naming Controllers
~~~~~~~~~~~~~~~~~~

Controllers are implemented as Python classes and are therefore expected to follow the PEP8 naming standard and be named in the StudlyCaps format (otherwise known as CamelCase). Additionally, while not strictly required, controller names usually contain the suffix ``Controller`` (e.g. ``UserProfileController``).

When the pybald route map is generated, the controller class name is converted to underscore_separated format and '_controller' is stripped if present. Following the example above, the route map would contain the identifier ``user_profile`` for the controller. When creating connections in the url mapping, the controller identifier would be used for the controller argument.

Naming Models
~~~~~~~~~~~~~

Models are also implemented as Python classes and are expected to follow the PEP8 style guide and be named in the StudlyCaps style. Model class names are usually expected to be singular nouns (User not Users).

When pybald models are synchronized with a databse, by default the underlying tables are named by converting the StudlyCaps class name into an underscore_separated form and pluralized. Therefore a ``UserProfile`` model will (by default) create a ``user_profiles`` database table. Obviously an explicit table name can also be provided to any model to override this default behavior.

Naming Modules
~~~~~~~~~~~~~~

All modules are expected to also follow the PEP8 style guide and be named in the underscore_separated style.

Structure of a Pybald Application
---------------------------------

A Pybald application is configured, at least partially, by the directory structure of the *project*. Unless overridden, the default pybald router behavior will look for python module files in certain paths and will import them which "activates" them for use.

``./app``
  This is the primary application directory containing the controllers, views and models
    ``./app/controllers``
      All controller files for the project
    ``./app/models``
      Models for the project
    ``./app/middleware``
      *optional* - Any project specific WSGI middleware
    ``./app/views``
      Templates for the project
    ``./app/urls.py``
      Url patterns to match against
``./public``
  Static content like images, css and javascript
``./project.py``
  Configuration file for the project.
``./environment.py``
  Local, environment-specific, configuration overrides (e.g. Production, Development, Test)
``./startup``
  Web server configuration, startup scripts.
``./utilities``
  Project utility scripts.
``./tmp``
  Temporary files
    ``./viewscache``
      *temporary* The template engine's file cache for views
``./wsgi``
  The directory containing the primary WSGI application
    ``./myapp.py``
      The WSGI app.


Most of your application code will be in the ``app`` directory which should contain at least these three directories ``controllers``, ``views``, and ``models``.


A Pybald application consists of the following parts:

* A webserver
* A *WSGI pipeline*

  * A Router/Dispatcher WSGI module
  * User defined controllers, models, and views
  * Any additional WSGI middleware

* Static content: images, css, javascript

The heart of a Pybald application is the *WSGI pipeline*. The pipeline is defined in the file ``./wsgi/myapp.py``. The WSGI pipeline is your application as well as how your webserver of choice will communicate with your application. `myapp.py` can be used to connect to any WSGI compliant webserver (Apache, nginx, uWSGI, etc...), or it can be run directly which invokes a built-in testing server from the command line.

.. code-block:: python

    # The main application pipeline
    # Include all WSGI middleware here. The order of
    # web transaction will flow from the bottom of this list
    # to the top, and then back out. The pybald Router
    # should usually be the first item listed.
    # ----------------------------------
    app = Router(routes=my_project.app.urls.map)
    # app = UserManager(app, user_class=User)
    # app = SessionManager(app, session_class=Session)
    # app = ErrorMiddleware(app, error_controller=None)
    # app = DbMiddleware(app)
    # ----------------------------------
    #    ↑↑↑                  ↓↓↓
    #    ↑↑↑                  ↓↓↓
    #   Request              Response


Invoking the development web server from the command line should look similar to starting the console (in fact the same code executes). The webserver log is dumped to the console so you can monitor transactions.

.. code-block:: sh

    ~/test_project$ python wsgi/myapp.py
    Route name Methods Path                       
    home               /                          
    base               /{controller}/{action}/{id}
                       /{controller}/{action}     
                       /{controller}              
                       /*(url)/                   
    serving on 0.0.0.0:8080 view at http://127.0.0.1:8080


.. _console:
The Pybald console
------------------

The pybald console allows you to interact with your program using the python REPL.

The console automatically loads the route mapping for your application as well as all of the models for your project. The console allows you to interact with your application directly, experiment with new functionality, play with models, and test and exercise the application.

It also includes a command history per-project.
