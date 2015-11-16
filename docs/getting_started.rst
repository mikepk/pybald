Quick Start
===============

Installing
------------

It's recommended that you use ``virtualenv`` to allow you to isolate experimenting with pybald (and its dependencies) from the rest of your python environment. First we setup a new virtualenv, then we install pybald, finally we copy the empty project_template to a new project name.

.. code-block:: sh

    ~$ virtualenv pyb_test
    New python executable in pyb_test/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    ~$ source ./pyb_test/bin/activate
    (pyb_test)~$ pip install pybald
    Downloading/unpacking pybald
      Downloading pybald-0.2.0.tar.gz
      Running setup.py egg_info for package pybald
     [...]
    Successfully installed Mako-1.0.1 MarkupSafe-0.23 PyExecJS-1.1.0 PyReact-0.5.2 SQLAlchemy-1.0.8 WTForms-2.0.2 WebOb-1.4.1 alembic-0.7.7 cssmin-0.2.0 lxml-3.4.4 pybald pybald-routes-2.11 repoze.lru-0.6 rjsmin-1.0.10 six-1.9.0 webassets-0.10.1
      Cleaning up...
    (pyb_test)~$ python sample.py console


Running your first Pybald Application
-------------------------------------

First copy the following code and save it as a file, say ``sample.py``. Don't choose 'pybald.py' since it will conflict with the pybald library name.

.. code-block:: python

    import pybald
    from pybald import context
    from pybald.core.controllers import Controller, action
    from pybald.core.router import Router

    # configure our pybald application
    pybald.configure()

    def map(urls):
        urls.connect('home', r'/', controller='home')

    class HomeController(Controller):
        @action
        def index(self, req):
            return "Hello!"

    app = Router(routes=map, controllers=[HomeController])

    if __name__ == "__main__":
        context.start(app)


To start the application from the command line type ``python sample.py console`` which starts the pybald :ref:`console <console>` for this project. The pybald console is a standard python REPL but also initializes your project, loads the application code, and allows you to interact with your application in various ways including simulating requests, exploring models, prototyping new functionality and other tasks. It's important to note that the application is the *same* application that runs when connected to the web server.

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

The console has a testing / convenience client ``c`` that allows you to issue web-like requests to your application. Here we've fetched the "/" url from the application and received a response. You can see some debug information is printed to the screen about what URL we fetched, what method and what controller and action were invoked. Finally we print the response from that url which is the simple web response message that pybald is working!

Boom! You're running a pybald application.

