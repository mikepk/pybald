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

