Quick Start
===============

Installing
------------

It's recommended that you use ``virtualenv`` to allow you to isolate experimenting with pybald (and its dependencies) from the rest of your python environment. First we setup a new virtualenv, then we install pybald, finally we copy the empty project_template to a new project name.

.. code-block:: sh

    ~$ virtualenv --no-site-packages pyb_test
    New python executable in pyb_test/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    ~$ source ./pyb_test/bin/activate
    (pyb_test)~$ pip install -e git+git://github.com/mikepk/pybald#egg=pybald
    Obtaining pybald from git+git://github.com/mikepk/pybald#egg=pybald
      Cloning git://github.com/mikepk/pybald to ./pyb_test/src/pybald
      Running setup.py egg_info for package pybald
     [...]
      Successfully installed pybald Routes FormAlchemy SqlAlchemy
      WebOb Eventlet Spawning Mako python-memcached Tempita WebHelpers 
      greenlet MarkupSafe
      Cleaning up...
    (pyb_test)~$ sudo cp -R pyb_test/src/pybald/pybald/project_template/ ./test_project
    (pyb_test)~$ cd test_project
    (pyb_test)~/test_project$ python project.py


Running your first Pybald Application
-------------------------------------

The command ``python project.py`` starts the pybald :ref:`console <console>` for this project. The console is a standard python console but also initializes your project, loads the application code, and allows you to interact with your application in various ways including simulating requests, exploring models, prototyping new functionality and other tasks.

.. code-block:: pycon

    Route name Methods Path                       
    home               /                          
    base               /{controller}/{action}/{id}
                       /{controller}/{action}     
                       /{controller}              
                       /*(url)/                   
    Welcome to the pybald interactive console
     ** project: test_project **
    >>> response = c.get("/")
    ============= / ==============
    Method: GET
    action: index
    controller: home
    >>> print response
    200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 18

    Pybald is working.

When debugging is turned on, the routing layer of Pybald will display all of the configured url routes for the project, then a small welcome message. Out of the box pybald is configured with a generic set of routes that allow for quick prototyping.

The console has a testing / convenience client ``c`` that allows you to issue simulated web requests to your application. Here we've fetched the "/" url from the application and received a response. You can see some debug information is printed to the screen about what URL we fetched, what method and what controller and action were invoked. Finally we print the response from that url which is the simple web response message that pybald is working!

Pow! You're running a pybald application.


Structure of a Pybald Application
---------------------------------

A Pybald application is configured, at least partially, by the directory structure of the *project*. The pybald router will look for files in certain paths and will "activate" them for use.

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