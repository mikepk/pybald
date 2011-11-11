Getting Started
===============

We'll start with a quick tutorial on running your first PyBald Web Application and then show how the various pieces work together.

Installation
------------

**!! Coming soon !!**


Running your first PyBald Application
-------------------------------------

**!! Coming soon !!**


Structure of a PyBald Application
---------------------------------

A PyBald application is configured, at least partially, by the directory structure. Placing files with certain naming conventions in certain paths will "activate" them for use.

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
``./content``
  Static content like images, css and javascript
``./project.py``
  Configuration file for the project. 
``./environment.py``
  Local, environment-specific, configuration overrides (e.g. Production, Development, Test)
``./startup``
  Web server configuration, startup scripts.
``./utilities``
  Project utility scripts.
``./viewscache``
  *temporary* The template engine's file cache for views
``./wsgi``
  The directory containing the primary WSGI application
    ``./app.py``
      The WSGI app.
      

Most of your application code will be in the ``app`` directory which contains three directories ``controllers``, ``views``, and ``models``.


A PyBald application consists of the following parts:

* A webserver
* A *WSGI pipeline*

  * A Router/Dispatcher WSGI module
  * User defined controllers, models, and views
  * Any additional WSGI middleware

* Static content: images, css, javascript

The heart of a PyBald application is the *WSGI pipeline*. The pipeline is defined in the file ``./wsgi-scripts/myapp.wsgi``. The WSGI pipeline is how your webserver will communicate with your application. `myapp.wsgi` can be used to connect to Apache, or it can be run directly which invokes the paste.httpserver from the command line. 

.. code-block:: python

  import site
  site.addsitedir(project_path)
  site.addsitedir(pybald_path)

  import project
  from pybald.core.Router import Router

  # create and load the url router
  url_route = Router()
  project.set_routes(url_route.map)
  url_route.load()

  # this is for apache or nginex
  # mod_wsgi calls 'application'
  application = url_route


