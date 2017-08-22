Quick Start
===============

Installing
------------

Using virtualenv
~~~~~~~~~~~~~~~~

While not strictly necessary, it is recommended that you use ``virtualenv`` to allow you to isolate experimenting with Pybald (and its dependencies) from the rest of your python environment.

First we setup a new virtualenv, activate it, then we install pybald.

.. code-block:: sh

    ~$ virtualenv pyb_test
    New python executable in pyb_test/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    ~$ source ./pyb_test/bin/activate
    (pyb_test)~$ pip install pybald
    Downloading/unpacking pybald
      Downloading pybald-X.X.X.tar.gz
      Running setup.py egg_info for package pybald
     [...]
    Successfully installed [various packages]
      Cleaning up...


Without virtualenv
~~~~~~~~~~~~~~~~~~

Just install pybald from pypi using pip.

.. code-block:: sh

    ~$ pip install pybald
    Downloading/unpacking pybald
      Downloading pybald-X.X.X.tar.gz
      Running setup.py egg_info for package pybald
     [...]
    Successfully installed [various packages]
      Cleaning up...

Running your first Pybald Application
-------------------------------------

First copy the following code and save it as a file, say ``sample.py``. Don't choose the name 'pybald.py' since it will conflict with the pybald library name but most any other name should be fine.

.. code-block:: python

    import pybald
    from pybald import context
    from pybald.core.controllers import Controller, action
    from pybald.core.router import Router

    # configure our pybald application
    pybald.configure(debug=True)

    def map(urls):
        urls.connect('home', r'/', controller='home')

    class HomeController(Controller):
        @action
        def index(self, req):
            return "Hello!"

    app = Router(routes=map, controllers=[HomeController])

    if __name__ == "__main__":
        context.start(app)


To start the application from the command line type ``python sample.py console`` which starts the pybald :ref:`console <console>` for this project. The pybald console is a standard python REPL but also initializes your project, loads the application code, and allows you to interact with your application in various ways including simulating requests, exploring models, prototyping new functionality, running a debugger and other tasks. The console also has some convenience functions, like saving a per-project history to allow "up arrow", tab completion and other history searches.

.. note::

    If, instead, you'd like to try the application from a web browser, you can also call ``python sample.py serve`` and that will run a simple development web server that you can connect to. You can see a simple help message for command line arguments by using ``python sample.py -h`` or ``python sample.py {COMMAND} -h``.

    It can be generally useful to be able to explore and introspect the application from a REPL to really learn how Pybald works.

    It's also important to note that the application that runs in the console is *exactly the same* as the application that runs when connected to the web server.

.. code-block:: pycon

    $ python sample.py console
    Route name Methods Path
    home               /   
    Welcome to the Pybald interactive console
     ** project: sample.py **
    >>>

When debug logging is turned on, the routing layer of Pybald will display all of the configured url routes for the project, then a small welcome message. In this case, we've only set up a single route for '/' connected to the home controller.

The console also loads a very simple testing / convenience client ``c`` that allows you to issue simulated web requests to your application using GET's and POST's.

.. code-block:: pycon

    $ python sample.py console
    Route name Methods Path
    home               /   
    Welcome to the Pybald interactive console
     ** project: sample.py **
    >>> resp = c.get('/')
    ====================================== / ======================================
    Method: GET
    action: index
    controller: home
    >>> print resp
    200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 6

    Hello!

Here we've fetched the "/" url from the application and received a response. You can see some debug information is printed to the screen about what URL we fetched, what method and what controller and action were matched/invoked. If any capture variables had been present, they would have been printed as well. Finally we print the response from that request which is the full web response (headers etc) and the simple text response message of "Hello". The ``resp`` object that is returned is an instance of a WebOb Response object. WebOb response objects have numerous useful attributes and methods. For example, you can get things like ``resp.headers``, ``resp.status``, ``resp.body`` to see some of the data available on the response.

.. code-block:: pycon

    >>> resp.headers
    ResponseHeaders([('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', '6')])
    >>> resp.status
    '200 OK'
    >>> resp.body
    'Hello!'

Boom! You're running a pybald application.

.. note::

    Most of the time you won't need to know or care, but an interesting detail worth mentioning at this point is that the ``response object`` is also a WSGI application just like the core pybald application. This allows for some interesting flexibility in chaining and re-routing application behavior. The response object will accept ``environ, start_response`` call signature just like the Router or any other WSGI app. Many of the interfaces of Pybald use the WSGI interace allowing for a great deal of flexibility.