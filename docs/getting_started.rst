Quick Start
===============

We'll start with a quick tutorial on running your first Pybald Web Application and then show how the various pieces work together.

Installing
------------

First we fetch and install pybald. This example uses ``virtualenv`` so you can isolate experimenting with pybald (and its dependencies) from the rest of your python environment. It's not required but recommended.

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

The command ``python project.py`` starts the pybald console for this project. The console is a standard python console but it also allows you to interact with your application in various ways including simulating requests, exploring models, prototyping new functionality and other tasks.

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

When debugging is turned on, the routing layer of Pybald will display all of the configured url routes for the project first, then a small welcome message.

The console has a testing / convenience client ``c`` that allows you to issue simulated web requests to your application. Here we've fetched the "/" url from the application and received a response. You can see some debug information is printed to the screen about what URL we fetched, what method and what controller and action were invoked. Finally we print the response from that url which is the simple web response message that pybald is working!

Pow! You're running a Pybald application, although not a very interesting one I'll grant you.




Structure of a Pybald Application
---------------------------------

A Pybald application is configured, at least partially, by the directory structure. Placing files with certain naming conventions in certain paths will "activate" them for use.

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
      

Most of your application code will be in the ``app`` directory which contains three directories ``controllers``, ``views``, and ``models``.


A Pybald application consists of the following parts:

* A webserver
* A *WSGI pipeline*

  * A Router/Dispatcher WSGI module
  * User defined controllers, models, and views
  * Any additional WSGI middleware

* Static content: images, css, javascript

The heart of a Pybald application is the *WSGI pipeline*. The pipeline is defined in the file ``./wsgi/myapp.py``. The WSGI pipeline is how your webserver will communicate with your application. `myapp.py` can be used to connect to Apache, or it can be run directly which invokes the paste.httpserver from the command line. 

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
    app = ErrorMiddleware(app, error_controller=None)
    app = DbMiddleware(app)
    # ----------------------------------
    #    ↑↑↑                  ↓↓↓
    #    ↑↑↑                  ↓↓↓
    #   Request              Response


